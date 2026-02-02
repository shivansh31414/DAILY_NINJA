# Azure Deployment Guide

## Prerequisites

- Azure CLI installed
- Azure subscription
- GitHub repository connected

## Services Required

1. **Azure Container Registry (ACR)** - Docker image storage
2. **Azure Database for PostgreSQL** - Managed database
3. **Azure Cache for Redis** - Managed cache
4. **Azure App Service / AKS** - Application hosting
5. **Azure Pipelines** - CI/CD automation
6. **Azure Service Bus** - Message queue for Celery

## Deployment Steps

### 1. Create Azure Resources

```bash
# Set variables
RESOURCE_GROUP="daily-ninja-rg"
LOCATION="eastus"
ACR_NAME="dailyninjaacr"
DB_NAME="daily-ninja-db"
REDIS_NAME="daily-ninja-redis"

# Create resource group
az group create --name $RESOURCE_GROUP --location $LOCATION

# Create Container Registry
az acr create --resource-group $RESOURCE_GROUP --name $ACR_NAME --sku Basic

# Create PostgreSQL
az postgres server create \
  --resource-group $RESOURCE_GROUP \
  --name $DB_NAME \
  --location $LOCATION \
  --admin-user adminuser \
  --admin-password YourPassword123!

# Create Redis
az redis create \
  --resource-group $RESOURCE_GROUP \
  --name $REDIS_NAME \
  --location $LOCATION \
  --sku Basic
```

### 2. Configure CI/CD Pipeline

Create `.github/workflows/deploy.yml` or use Azure Pipelines YAML.

### 3. Deploy to App Service

```bash
# Create App Service Plan
az appservice plan create \
  --name daily-ninja-plan \
  --resource-group $RESOURCE_GROUP \
  --sku B2 --is-linux

# Create Web App
az webapp create \
  --resource-group $RESOURCE_GROUP \
  --plan daily-ninja-plan \
  --name daily-ninja-app \
  --deployment-container-image-name-user dailyninjaacr
```

## Environment Variables

Set these in Azure App Service Configuration:

```
DATABASE_URL=postgresql://user:pass@host/dbname
REDIS_URL=redis://host:6379/0
CELERY_BROKER_URL=redis://host:6379/1
SECRET_KEY=your-secret-key
ENV=production
```

## Monitoring

```bash
# View logs
az webapp log tail --resource-group $RESOURCE_GROUP --name daily-ninja-app

# Application Insights
az monitor app-insights create \
  --resource-group $RESOURCE_GROUP \
  --application-type web \
  --display-name daily-ninja-insights
```

## Scaling

```bash
# Auto-scale configuration
az monitor autoscale create \
  --resource-group $RESOURCE_GROUP \
  --resource-name daily-ninja-plan \
  --resource-type "Microsoft.Web/serverfarms" \
  --min-count 1 \
  --max-count 5
```
