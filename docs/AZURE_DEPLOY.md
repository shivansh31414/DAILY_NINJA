# Deploying Daily Ninja to Azure Web App for Containers

## Prerequisites
- Azure CLI logged in (`az login`)
- Docker installed
- Azure DevOps service connections for ACR and Azure subscription

## 1. Create Resource Group and ACR

```bash
export AZURE_RESOURCE_GROUP=daily-ninja-rg
export AZURE_LOCATION=eastus
export ACR_NAME=dailyninjaacr

az group create --name $AZURE_RESOURCE_GROUP --location $AZURE_LOCATION
az acr create --resource-group $AZURE_RESOURCE_GROUP --name $ACR_NAME --sku Basic
```

Or run:

```bash
bash scripts/azure/01_setup_rg_acr.sh
```

## 2. Build, tag, and push image to ACR

```bash
export IMAGE_NAME=daily-ninja
export IMAGE_TAG=latest
bash scripts/azure/02_build_push.sh
```

## 3. Deploy container to Azure Web App for Containers

```bash
export AZURE_WEBAPP_NAME=daily-ninja-app
export APP_SERVICE_PLAN=daily-ninja-plan
bash scripts/azure/03_deploy_webapp.sh
```

## 4. Configure environment variables with Key Vault references

```bash
az webapp config appsettings set \
  --resource-group $AZURE_RESOURCE_GROUP \
  --name daily-ninja-app \
  --settings \
    WEBSITES_PORT=8000 \
    FLASK_ENV=production \
    SECRET_KEY="@Microsoft.KeyVault(SecretUri=https://daily-ninja-kv.vault.azure.net/secrets/SECRET_KEY/)" \
    JWT_SECRET_KEY="@Microsoft.KeyVault(SecretUri=https://daily-ninja-kv.vault.azure.net/secrets/JWT_SECRET_KEY/)" \
    DATABASE_URL="@Microsoft.KeyVault(SecretUri=https://daily-ninja-kv.vault.azure.net/secrets/DATABASE_URL/)"
```

## 5. Enable logging and monitoring with Application Insights

```bash
az monitor app-insights component create \
  --app daily-ninja-ai \
  --location $AZURE_LOCATION \
  --resource-group $AZURE_RESOURCE_GROUP

APPINSIGHTS_CONNECTION_STRING=$(az monitor app-insights component show \
  --app daily-ninja-ai \
  --resource-group $AZURE_RESOURCE_GROUP \
  --query connectionString -o tsv)

az webapp config appsettings set \
  --resource-group $AZURE_RESOURCE_GROUP \
  --name daily-ninja-app \
  --settings APPLICATIONINSIGHTS_CONNECTION_STRING="$APPINSIGHTS_CONNECTION_STRING"
```

## 6. Configure autoscaling for App Service Plan

```bash
bash scripts/azure/05_configure_autoscale.sh
```

## 7. CI/CD pipeline

`azure-pipelines.yml` includes stages:
- Build
- Test (lint + pytest + unittest + coverage)
- Docker Build
- Push
- Deploy

## 8. Verify deployment

Primary URL:

```text
https://daily-ninja-app.azurewebsites.net
```

Manual checks:

```bash
curl -fsS https://daily-ninja-app.azurewebsites.net/health
curl -fsS https://daily-ninja-app.azurewebsites.net/
```

Run post-deploy integration tests:

```bash
export DAILY_NINJA_BASE_URL=https://daily-ninja-app.azurewebsites.net
python -m pytest daily_ninja_python/tests/integration/test_post_deploy.py -q
```

Or run:

```bash
bash scripts/azure/04_verify_deployment.sh
```

## Troubleshooting if app is unreachable

If `https://daily-ninja-app.azurewebsites.net` does not resolve or returns errors, run:

```bash
az webapp show --resource-group $AZURE_RESOURCE_GROUP --name daily-ninja-app --query defaultHostName -o tsv
az webapp config container show --resource-group $AZURE_RESOURCE_GROUP --name daily-ninja-app
az webapp config appsettings list --resource-group $AZURE_RESOURCE_GROUP --name daily-ninja-app
az webapp log config --name daily-ninja-app --resource-group $AZURE_RESOURCE_GROUP --docker-container-logging filesystem
az webapp log tail --name daily-ninja-app --resource-group $AZURE_RESOURCE_GROUP
```

Validate image availability in ACR:

```bash
az acr repository list --name $ACR_NAME -o table
az acr repository show-tags --name $ACR_NAME --repository daily-ninja -o table
```

Check runtime health endpoint from inside your network path:

```bash
curl -v https://daily-ninja-app.azurewebsites.net/health
```

If Key Vault references are used, confirm app identity access:

```bash
az webapp identity show --resource-group $AZURE_RESOURCE_GROUP --name daily-ninja-app
az keyvault show --name daily-ninja-kv --query properties.vaultUri -o tsv
```

## Reviewer checklist for this PR

Run these commands from repo root:

```bash
bash scripts/azure/01_setup_rg_acr.sh
bash scripts/azure/02_build_push.sh
bash scripts/azure/03_deploy_webapp.sh
bash scripts/azure/05_configure_autoscale.sh
bash scripts/azure/04_verify_deployment.sh
```

Then confirm:

```bash
curl -fsS https://daily-ninja-app.azurewebsites.net/health
python -m pytest daily_ninja_python/tests/integration/test_post_deploy.py -q
```
