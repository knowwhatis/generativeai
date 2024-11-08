# a. Create PR checks trigger
resource "google_cloudbuild_trigger" "pr_checks" {
  name            = "pr-checks"
  project         = var.cicd_runner_project_id
  location        = var.region
  description     = "Trigger for PR checks"
  service_account = resource.google_service_account.cicd_runner_sa.id

  repository_event_config {
    repository = "projects/${var.cicd_runner_project_id}/locations/${var.region}/connections/${var.host_connection_name}/repositories/${var.repository_name}"
    pull_request {
      branch = "main"
    }
  }

  filename = "deployment/ci/pr_checks.yaml"
  included_files = [
    "app/**",
    "tests/**",
    "deployment/**",
    "poetry.lock"
  ]

  # include_build_logs = "INCLUDE_BUILD_LOGS_WITH_STATUS" # this is only supported in GITHUB repo type
  depends_on         = [resource.google_project_service.cicd_services, resource.google_project_service.shared_services]
}

# b. Create CD pipeline trigger
resource "google_cloudbuild_trigger" "cd_pipeline" {
  name            = "cd-pipeline"
  project         = var.cicd_runner_project_id
  location        = var.region
  service_account = resource.google_service_account.cicd_runner_sa.id
  description     = "Trigger for CD pipeline"

  repository_event_config {
    repository = "projects/${var.cicd_runner_project_id}/locations/${var.region}/connections/${var.host_connection_name}/repositories/${var.repository_name}"
    push {
      branch = "main"
    }
  }

  filename = "deployment/cd/staging.yaml"
  included_files = [
    "app/**",
    "tests/**",
    "deployment/**",
    "poetry.lock"
  ]
  substitutions = {
    _STAGING_PROJECT_ID            = var.staging_project_id
    _PROD_PROJECT_ID               = var.prod_project_id
    _BUCKET_NAME_LOAD_TEST_RESULTS = resource.google_storage_bucket.bucket_load_test_results.name
    _ARTIFACT_REGISTRY_REPO_NAME   = var.artifact_registry_repo_name
    _CLOUD_RUN_APP_SA_NAME         = var.cloud_run_app_sa_name
    _SINGLE_REGION                 = var.region
    _MULTI_REGION                  = var.location
    _DATA_INGESTION_BUCKET_PREF    = var.data_ingestion_bucket_name_prefix                                        # ! Specific to Vertex AI Search pattern 
    _DATA_INGESTION_APP_NAME       = var.data_ingestion_app_name                                                  # ! Specific to Vertex AI Search pattern 
    _DATA_STORE_ID                 = resource.google_discovery_engine_data_store.data_store_staging.data_store_id # ! Specific to Vertex AI Search pattern 
    _VERTEX_AI_APP_SA_NAME         = var.vertexai_pipeline_app_sa_name                                            # ! Specific to Vertex AI Search pattern 
  }

  depends_on         = [resource.google_project_service.cicd_services, resource.google_project_service.shared_services]
  
}

# c. Create Deploy to production trigger
resource "google_cloudbuild_trigger" "deploy_to_prod_pipeline" {
  name            = "deploy-to-prod-pipeline"
  project         = var.cicd_runner_project_id
  location        = var.region
  description     = "Trigger for deployment to production"
  service_account = resource.google_service_account.cicd_runner_sa.id
  repository_event_config {
    repository = "projects/${var.cicd_runner_project_id}/locations/${var.region}/connections/${var.host_connection_name}/repositories/${var.repository_name}"
  }
  filename           = "deployment/cd/deploy-to-prod.yaml"
  approval_config {
    approval_required = true
  }
  substitutions = {
    _DATA_STORE_ID = resource.google_discovery_engine_data_store.data_store_prod.data_store_id
    _SINGLE_REGION = var.region
    _MULTI_REGION  = var.location
  }
  depends_on = [resource.google_project_service.cicd_services, resource.google_project_service.shared_services]

}
