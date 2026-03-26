#!/usr/bin/env bash
set -euo pipefail

: "${AZURE_RESOURCE_GROUP:=daily-ninja-rg}"
: "${AZURE_LOCATION:=eastus}"
: "${ACR_NAME:=dailyninjaacr}"

az login
az group create --name "$AZURE_RESOURCE_GROUP" --location "$AZURE_LOCATION"
az acr create --resource-group "$AZURE_RESOURCE_GROUP" --name "$ACR_NAME" --sku Basic
az acr show --name "$ACR_NAME" --query loginServer -o tsv
