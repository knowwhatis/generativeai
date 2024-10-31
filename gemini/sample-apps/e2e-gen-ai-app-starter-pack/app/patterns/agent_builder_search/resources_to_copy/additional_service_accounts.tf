
# Service account to run VertexAI pipeline
# ! Specific to VertexAI Search pattern 
resource "google_service_account" "vertexai_pipeline_app_sa" {
  for_each = local.project_ids

  account_id   = var.vertexai_pipeline_app_sa_name
  display_name = "VertexAI Pipeline app SA"
  project      = each.value
  depends_on   = [resource.google_project_service.cicd_services, resource.google_project_service.shared_services]
}
