# ! Specific to Vertex AI Search pattern 
# -------------------------------------

provider "google" {
  alias                 = "staging_billing_override"
  billing_project       = var.staging_project_id
  user_project_override = true
}

provider "google" {
  alias                 = "prod_billing_override"
  billing_project       = var.prod_project_id
  user_project_override = true
}

resource "google_discovery_engine_data_store" "data_store_staging" {
  location                    = var.location
  project                     = var.staging_project_id
  data_store_id               = "datastore-${var.staging_project_id}-staging"
  display_name                = "datastore-staging"
  industry_vertical           = "GENERIC"
  content_config              = "NO_CONTENT"
  solution_types              = ["SOLUTION_TYPE_SEARCH"]
  create_advanced_site_search = false
  provider                    = google.staging_billing_override
}
resource "google_discovery_engine_search_engine" "search_engine_staging" {
  project        = var.staging_project_id
  engine_id      = "search_engine-${var.staging_project_id}-staging"
  collection_id  = "default_collection"
  location       = google_discovery_engine_data_store.data_store_staging.location
  display_name   = "Search Engine App Staging"
  data_store_ids = [google_discovery_engine_data_store.data_store_staging.data_store_id]
  search_engine_config {
    search_tier = "SEARCH_TIER_ENTERPRISE"
  }
  provider = google.staging_billing_override
}


resource "google_discovery_engine_data_store" "data_store_prod" {
  location                    = var.location
  project                     = var.prod_project_id
  data_store_id               = "datastore-${var.prod_project_id}-prod"
  display_name                = "datastore-prod"
  industry_vertical           = "GENERIC"
  content_config              = "NO_CONTENT"
  solution_types              = ["SOLUTION_TYPE_SEARCH"]
  create_advanced_site_search = false
  provider                    = google.prod_billing_override
}
resource "google_discovery_engine_search_engine" "search_engine_prod" {
  project        = var.prod_project_id
  engine_id      = "search_engine-${var.prod_project_id}-prod"
  collection_id  = "default_collection"
  location       = google_discovery_engine_data_store.data_store_prod.location
  display_name   = "Search Engine App Prod"
  data_store_ids = [google_discovery_engine_data_store.data_store_prod.data_store_id]
  search_engine_config {
    search_tier = "SEARCH_TIER_ENTERPRISE"
  }
  provider = google.prod_billing_override
}

data "google_project" "staging_project" {
  project_id = var.staging_project_id
}
data "google_project" "prod_project" {
  project_id = var.prod_project_id
}
