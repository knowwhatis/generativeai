# ! Specific to VertexAI Search pattern

variable "vertexai_pipeline_app_sa_name" {
  description = "Service account name to be used for the VertexAI service"
  type        = string
  default     = "data-ingestion-vertexai-sa"
}

variable "location" {
  type        = string
  description = "Google Cloud region for resource deployment."
  default     = "us"
}

variable "vertexai_roles" {
  description = "List of roles to assign to the VertexAI runner service account"
  type        = list(string)
  default = [
    "roles/storage.admin",
    "roles/run.invoker",
    "roles/aiplatform.user",
    "roles/discoveryengine.admin",
    "roles/logging.logWriter",
    "roles/artifactregistry.writer",
  ]
}

variable "data_ingestion_bucket_name_prefix" {
  description = "Prefix of name for bucket to be used for data ingestion"
  type = string
  default = "default-bucket-prefix-for-ingestion"
}

variable "data_ingestion_app_name" {
  description = "The name of the cloud run service for data ingestion"
  type = string
  default = "data-ingestion-app"
}

