#!/bin/bash

# Add additional substitutions to the build_triggers.tf file
sed -i "$(grep -n "substitutions_cd_pipeline_triggers" deployment/terraform/build_triggers.tf | cut -d: -f1)r app/patterns/agent_builder_search/resources_to_copy/deployment/terraform/substitutions_cd_pipeline_triggers.tf_updates" deployment/terraform/build_triggers.tf
sed -i "$(grep -n "substitutions_deploy_to_prod_pipeline_triggers" deployment/terraform/build_triggers.tf | cut -d: -f1)r app/patterns/agent_builder_search/resources_to_copy/deployment/terraform/substitutions_deploy_to_prod_pipeline_triggers.tf_updates" deployment/terraform/build_triggers.tf

# Add new values at the end of several tf files.
cat app/patterns/agent_builder_search/resources_to_copy/deployment/terraform/additional_iam.tf_updates >> deployment/terraform/iam.tf
cat app/patterns/agent_builder_search/resources_to_copy/deployment/terraform/additional_service_accounts.tf_updates >> deployment/terraform/service_accounts.tf
cat app/patterns/agent_builder_search/resources_to_copy/deployment/terraform/additional_storage.tf_updates >> deployment/terraform/storage.tf
cat app/patterns/agent_builder_search/resources_to_copy/deployment/terraform/additional_variables.tf_updates >> deployment/terraform/variables.tf
cat app/patterns/agent_builder_search/resources_to_copy/deployment/terraform/additional_env.tfvars_updates >> deployment/terraform/vars/env.tfvars
# TODO: Do we need the same for deployment/terraform/dev ?

# Add new tf files to the deployment folder
mv app/patterns/agent_builder_search/resources_to_copy/deployment/terraform/data_store.tf_updates deployment/terraform/data_store.tf
# replace tf file with different substitution parameter names

# replace the old files with the new ones and add the ingestion logic
mv deployment/cd/deploy-to-prod.yaml deployment/cd/unused-deploy-to-prod.yaml
mv deployment/cd/staging.yaml deployment/cd/unused-staging.yaml
mv app/patterns/agent_builder_search/resources_to_copy/deployment/cd/deploy-to-prod.yaml deployment/cd/deploy-to-prod.yaml
mv app/patterns/agent_builder_search/resources_to_copy/deployment/cd/staging.yaml deployment/cd/staging.yaml
mkdir app/data_ingestion
mv app/patterns/agent_builder_search/resources_to_copy/data_ingestion/pipeline.py app/data_ingestion/pipeline.py
mv app/patterns/agent_builder_search/resources_to_copy/data_ingestion/ingestion_component.py app/data_ingestion/ingestion_component.py