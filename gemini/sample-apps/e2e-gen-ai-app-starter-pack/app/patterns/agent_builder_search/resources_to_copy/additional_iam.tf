
# 5. Grant Vertex AI SA the required permissions to run the ingestion
# ! Specific to Vertex AI Search pattern 
resource "google_project_iam_member" "vertexai_pipeline_sa_roles" {
  for_each = {
    for pair in setproduct(keys(local.project_ids), var.vertexai_roles) :
    join(",", pair) => {
      project = local.project_ids[pair[0]]
      role    = pair[1]
    }
  }

  project    = each.value.project
  role       = each.value.role
  member     = "serviceAccount:${google_service_account.vertexai_pipeline_app_sa[split(",", each.key)[0]].email}"
  depends_on = [resource.google_project_service.cicd_services, resource.google_project_service.shared_services]
}
