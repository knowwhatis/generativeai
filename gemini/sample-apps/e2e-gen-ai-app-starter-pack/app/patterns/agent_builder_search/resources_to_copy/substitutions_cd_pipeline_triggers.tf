    _LOCATION                      = var.location
    _DATA_INGESTION_BUCKET_PREF    = var.data_ingestion_bucket_name_prefix # ! Specific to VertexAI Search pattern 
    _DATA_INGESTION_APP_NAME       = var.data_ingestion_app_name # ! Specific to VertexAI Search pattern 
    _DATA_STORE_ID                 = resource.google_discovery_engine_data_store.data_store_staging.data_store_id # ! Specific to VertexAI Search pattern 
    _VERTEX_AI_APP_SA_NAME        = var.vertexai_pipeline_app_sa_name # ! Specific to VertexAI Search pattern 
