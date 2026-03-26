#!/usr/bin/env bash
set -euo pipefail

: "${AZURE_RESOURCE_GROUP:=daily-ninja-rg}"
: "${ACR_NAME:=dailyninjaacr}"
: "${IMAGE_NAME:=daily-ninja}"
: "${IMAGE_TAG:=latest}"

ACR_LOGIN_SERVER=$(az acr show --name "$ACR_NAME" --resource-group "$AZURE_RESOURCE_GROUP" --query loginServer -o tsv)
az acr login --name "$ACR_NAME"

docker build -f docker/Dockerfile.azure -t "$IMAGE_NAME:$IMAGE_TAG" .
docker tag "$IMAGE_NAME:$IMAGE_TAG" "$ACR_LOGIN_SERVER/$IMAGE_NAME:$IMAGE_TAG"
docker push "$ACR_LOGIN_SERVER/$IMAGE_NAME:$IMAGE_TAG"

echo "Pushed image: $ACR_LOGIN_SERVER/$IMAGE_NAME:$IMAGE_TAG"
