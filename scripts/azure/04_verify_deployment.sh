#!/usr/bin/env bash
set -euo pipefail

: "${DEPLOYED_URL:=https://daily-ninja-app.azurewebsites.net}"
: "${AZURE_RESOURCE_GROUP:=daily-ninja-rg}"
: "${AZURE_WEBAPP_NAME:=daily-ninja-app}"
: "${ACR_NAME:=dailyninjaacr}"

if ! curl -fsS "$DEPLOYED_URL/health"; then
	echo "Health check failed for $DEPLOYED_URL"
	echo "Run troubleshooting:"
	echo "az webapp show --resource-group $AZURE_RESOURCE_GROUP --name $AZURE_WEBAPP_NAME --query defaultHostName -o tsv"
	echo "az webapp config container show --resource-group $AZURE_RESOURCE_GROUP --name $AZURE_WEBAPP_NAME"
	echo "az webapp config appsettings list --resource-group $AZURE_RESOURCE_GROUP --name $AZURE_WEBAPP_NAME"
	echo "az webapp log tail --name $AZURE_WEBAPP_NAME --resource-group $AZURE_RESOURCE_GROUP"
	echo "az acr repository list --name $ACR_NAME -o table"
	exit 1
fi

curl -fsS "$DEPLOYED_URL/"

export DAILY_NINJA_BASE_URL="$DEPLOYED_URL"
python -m pytest daily_ninja_python/tests/integration/test_post_deploy.py -q

echo "Deployment verification passed for $DEPLOYED_URL"
