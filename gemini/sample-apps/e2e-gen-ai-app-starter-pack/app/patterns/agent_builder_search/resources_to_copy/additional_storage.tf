
# ! Specific to VertexAI Search pattern 
resource "google_storage_bucket" "data_ingestion_bucket" {
  for_each                    = toset(local.deploy_projects)
  name                        = "${var.data_ingestion_bucket_name_prefix}-${each.value}"
  location                    = var.region
  project                     = each.value
  uniform_bucket_level_access = true
  force_destroy               = true

  depends_on = [resource.google_project_service.cicd_services, resource.google_project_service.shared_services]
}

# ! Specific to VertexAI Search pattern 
resource "google_storage_bucket" "data_ingestion_pipeline_artifacts_bucket" {
  for_each                    = toset(local.deploy_projects)
  name                        = "${var.data_ingestion_bucket_name_prefix}-${each.value}-pipeline-artifacts"
  location                    = var.region
  project                     = each.value
  uniform_bucket_level_access = true
  force_destroy               = true

  depends_on = [resource.google_project_service.cicd_services, resource.google_project_service.shared_services]
}
