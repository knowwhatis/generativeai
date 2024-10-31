


In order to implement data ingestion for the datastore, you need to replace some of the 
existing files with new ones provided in the resources_to_copy folder

```bash

# Add additional substitutions to the build_triggers.tf file
sed -i "s/# To be extended for ingestion pipelines. Do not remove this line./$(cat app/patterns/agent_builder_search/resources_to_copy/substitutions_cd_pipeline_triggers.tf)/g" deployment/terraform/build_triggers.tf
sed -i "s/# To be replaced for ingestion pipelines. Do not remove this line./$(cat app/patterns/agent_builder_search/resources_to_copy/substitutions_deploy_to_prod_pipeline_triggers.tf)/g" deployment/terraform/build_triggers.tf

# Add new values at the end of several tf files.
cat app/patterns/agent_builder_pattern/resources_to_copy/additional_iam.tf >> deployment/terraform/vars/iam.tf
cat app/patterns/agent_builder_pattern/resources_to_copy/additional_service_accounts.tf >> deployment/terraform/vars/service_accounts.tf
cat app/patterns/agent_builder_pattern/resources_to_copy/additional_storage.tf >> deployment/terraform/vars/storage.tf
cat app/patterns/agent_builder_pattern/resources_to_copy/additional_variables.tf >> deployment/terraform/vars/variables.tf
cat app/patterns/agent_builder_pattern/resources_to_copy/additional_env.tfvars >> deployment/terraform/vars/env.tfvars
# TODO: Do we need the same for deployment/terraform/dev ?


# Add new tf files to the deployment folder
mv app/patterns/agent_builder_search/resources_to_copy/main.tf deployment/terraformy/main.tf
mv app/patterns/agent_builder_search/resources_to_copy/artifact_registry.tf deployment/terraformy/artifact_registry.tf
mv app/patterns/agent_builder_search/resources_to_copy/backend.tf deployment/terraformy/backend.tf
mv app/patterns/agent_builder_search/resources_to_copy/backend.tf deployment/terraformy/data_store.tf

# replace the old files with the new ones and add the ingestion logic
mv deployment/cd/deploy-to-prod.yaml deployment/cd/unused-deploy-to-prod.yaml
mv deployment/cd/staging.yaml deployment/cd/unused-staging.yaml
mv app/patterns/agent_builder_pattern/resources_to_copy/deploy-to-prod.yaml deployment/cd/deploy-to-prod.yaml
mv app/patterns/agent_builder_pattern/resources_to_copy/staging.yaml deployment/cd/staging.yaml
mv app/patterns/agent_builder_pattern/resources_to_copy/pipeline.py data_ingestion/pipeline.py
mv app/patterns/agent_builder_pattern/resources_to_copy/ingestion_component.py data_ingestion/ingestion_component.py
```


TODO: Replace the pip calls by poetry libs in yaml files.