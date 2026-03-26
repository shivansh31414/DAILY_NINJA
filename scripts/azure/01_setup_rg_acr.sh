#!/usr/bin/env bash
set -euo pipefail

: "${AZURE_RESOURCE_GROUP:=daily-ninja-rg}"
: "${AZURE_LOCATION:=eastus}"
: "${ACR_NAME:=dailyninjaacr}"

az login
az group create --name "$AZURE_RESOURCE_GROUP" --location "$AZURE_LOCATION" --output table

if ! az acr show --name "$ACR_NAME" --resource-group "$AZURE_RESOURCE_GROUP" >/dev/null 2>&1; then
	az acr create --resource-group "$AZURE_RESOURCE_GROUP" --name "$ACR_NAME" --sku Basic --output table
else
	echo "ACR $ACR_NAME already exists in $AZURE_RESOURCE_GROUP"
fi

az acr show --name "$ACR_NAME" --resource-group "$AZURE_RESOURCE_GROUP" --query "{name:name,loginServer:loginServer,sku:sku.name}" --output table
