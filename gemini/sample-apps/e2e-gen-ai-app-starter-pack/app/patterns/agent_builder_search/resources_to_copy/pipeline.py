# install kfp  google-cloud-pipeline-components
import os
from google.cloud import aiplatform
from kfp import compiler, dsl
from app.data_ingestion.ingestion_component import ingest_into_datastore

project_id = os.getenv("PROJECT_ID", "No project id set")
region_vertex = os.getenv("SINGLE_REGION", "No Vertex AI region set")
region_search = os.getenv("MULTI_REGION", "No agent builder region set")
input_bucket = os.getenv("INPUT_BUCKET", "No input bucket set")
data_store_id = os.getenv("DATA_STORE_ID", "No agent builder data store id set")
service_account = os.getenv("SERVICE_ACCOUNT", "No service account set")
pipeline_root = os.getenv("PIPELINE_ARTIFACT_OUTPUT", "No pipeline artifact output set")
cron_schedule = os.getenv("CRON_SCHEDULE", "No cron schedule set")

pipeline_root = f"gs://{pipeline_root}/pipeline_root/"

print("project_id: ", project_id)
print("region_vertex: ", region_vertex)
print("region_search: ", region_search)
print("input_bucket: ", input_bucket)
print("data_store_id: ", data_store_id)
print("service_account: ", service_account)
print("pipeline_root: ", pipeline_root)
print("cron_schedule: ", cron_schedule)


@dsl.pipeline(
    name="datastore-ingestion-pipeline",
    description="A pipeline to run ingestion of new data into the datastore",
    pipeline_root=pipeline_root,
)
def pipeline(
    project_id: str,
    region_vertex: str,
    region_search: str,
    input_bucket: str,
    data_store_id: str,
) -> None:
    ingest_into_datastore(
        project_id=project_id,
        region_vertex=region_vertex,
        region_search=region_search,
        input_bucket=input_bucket,
        data_store_id=data_store_id,
    )


compiler.Compiler().compile(
    pipeline_func=pipeline, package_path="ingestion_pipeline.json"
)


DISPLAY_NAME = "ingestion_pipeline_job"

job = aiplatform.PipelineJob(
    display_name=DISPLAY_NAME,
    template_path="ingestion_pipeline.json",
    pipeline_root=pipeline_root,
    project=project_id,
    location=region_vertex,
    parameter_values={
        "project_id": project_id,
        "region_vertex": region_vertex,
        "region_search": region_search,
        "input_bucket": input_bucket,
        "data_store_id": data_store_id,
    },
)

pipeline_job_schedule = aiplatform.PipelineJobSchedule(
    pipeline_job=job,
    display_name="Weekly Ingestion Job",
    credentials=job.credentials,
    project=job.project,
    location=job.location,
)

schedule_list = pipeline_job_schedule.list(
    filter='display_name="Weekly Ingestion Job"',
    project=project_id,
    location=region_vertex,
)
print("Schedule lists found: ", schedule_list)
if not schedule_list:
    pipeline_job_schedule.create(cron=cron_schedule, service_account=service_account)
    print("Schedule created")
else:
    schedule_list[0].update(cron=cron_schedule)
    print("Schedule updated")
    for schedule in schedule_list[1:]:
        print("Duplicate schedule found, deleting it")
        schedule.delete()
