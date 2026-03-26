#!/usr/bin/env bash
set -euo pipefail

: "${AZURE_RESOURCE_GROUP:=daily-ninja-rg}"
: "${APP_SERVICE_PLAN:=daily-ninja-plan}"

PLAN_ID=$(az appservice plan show --resource-group "$AZURE_RESOURCE_GROUP" --name "$APP_SERVICE_PLAN" --query id -o tsv)

az monitor autoscale create \
  --resource-group "$AZURE_RESOURCE_GROUP" \
  --resource "$PLAN_ID" \
  --resource-type Microsoft.Web/serverfarms \
  --name "${APP_SERVICE_PLAN}-autoscale" \
  --min-count 1 \
  --max-count 3 \
  --count 1

az monitor autoscale rule create \
  --resource-group "$AZURE_RESOURCE_GROUP" \
  --autoscale-name "${APP_SERVICE_PLAN}-autoscale" \
  --condition "Percentage CPU > 70 avg 5m" \
  --scale out 1

az monitor autoscale rule create \
  --resource-group "$AZURE_RESOURCE_GROUP" \
  --autoscale-name "${APP_SERVICE_PLAN}-autoscale" \
  --condition "Percentage CPU < 30 avg 10m" \
  --scale in 1
