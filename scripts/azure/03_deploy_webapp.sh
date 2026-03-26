#!/usr/bin/env bash
set -euo pipefail

: "${AZURE_RESOURCE_GROUP:=daily-ninja-rg}"
: "${AZURE_LOCATION:=eastus}"
: "${AZURE_WEBAPP_NAME:=daily-ninja-app}"
: "${APP_SERVICE_PLAN:=daily-ninja-plan}"
: "${ACR_NAME:=dailyninjaacr}"
: "${IMAGE_NAME:=daily-ninja}"
: "${IMAGE_TAG:=latest}"
: "${KEY_VAULT_SECRET_KEY_URI:=https://daily-ninja-kv.vault.azure.net/secrets/SECRET_KEY/}"
: "${KEY_VAULT_JWT_SECRET_KEY_URI:=https://daily-ninja-kv.vault.azure.net/secrets/JWT_SECRET_KEY/}"
: "${KEY_VAULT_DATABASE_URL_URI:=https://daily-ninja-kv.vault.azure.net/secrets/DATABASE_URL/}"
: "${APPLICATIONINSIGHTS_CONNECTION_STRING:=}"

ACR_LOGIN_SERVER=$(az acr show --name "$ACR_NAME" --resource-group "$AZURE_RESOURCE_GROUP" --query loginServer -o tsv)

az appservice plan create \
  --name "$APP_SERVICE_PLAN" \
  --resource-group "$AZURE_RESOURCE_GROUP" \
  --location "$AZURE_LOCATION" \
  --is-linux \
  --sku S1

az webapp create \
  --resource-group "$AZURE_RESOURCE_GROUP" \
  --plan "$APP_SERVICE_PLAN" \
  --name "$AZURE_WEBAPP_NAME" \
  --deployment-container-image-name "$ACR_LOGIN_SERVER/$IMAGE_NAME:$IMAGE_TAG"

az webapp config container set \
  --resource-group "$AZURE_RESOURCE_GROUP" \
  --name "$AZURE_WEBAPP_NAME" \
  --container-image-name "$ACR_LOGIN_SERVER/$IMAGE_NAME:$IMAGE_TAG" \
  --container-registry-url "https://$ACR_LOGIN_SERVER"

az webapp config appsettings set \
  --resource-group "$AZURE_RESOURCE_GROUP" \
  --name "$AZURE_WEBAPP_NAME" \
  --settings \
    WEBSITES_PORT=8000 \
    FLASK_ENV=production \
    APPLICATIONINSIGHTS_CONNECTION_STRING="$APPLICATIONINSIGHTS_CONNECTION_STRING" \
    SECRET_KEY="@Microsoft.KeyVault(SecretUri=$KEY_VAULT_SECRET_KEY_URI)" \
    JWT_SECRET_KEY="@Microsoft.KeyVault(SecretUri=$KEY_VAULT_JWT_SECRET_KEY_URI)" \
    DATABASE_URL="@Microsoft.KeyVault(SecretUri=$KEY_VAULT_DATABASE_URL_URI)"

az webapp show --resource-group "$AZURE_RESOURCE_GROUP" --name "$AZURE_WEBAPP_NAME" --query defaultHostName -o tsv
