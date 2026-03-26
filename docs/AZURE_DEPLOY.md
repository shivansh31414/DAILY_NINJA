# Deploying Daily Ninja to Azure Web App for Containers

## Prerequisites
- Azure CLI installed and logged in
- Azure subscription and resource group
- Docker installed (for local builds)
- (Optional) Azure Container Registry (ACR) if using private images

## 1. Build and Push Docker Image

```bash
# Build Docker image
cd DAILY_NINJA
az acr login --name <your-acr-name>
docker build -f docker/Dockerfile.azure -t <your-acr-login-server>/daily-ninja:latest .
# Push to ACR
docker push <your-acr-login-server>/daily-ninja:latest
```

## 2. Provision Azure Resources (Bicep or ARM)

```bash
# Bicep
az deployment group create \
  --resource-group <your-rg> \
  --template-file infra/bicep/main.bicep \
  --parameters appServiceName=<your-app-name> keyVaultName=<your-kv-name> storageName=<yourstorage>

# ARM
az deployment group create \
  --resource-group <your-rg> \
  --template-file infra/arm/main.json \
  --parameters appServiceName=<your-app-name> keyVaultName=<your-kv-name> storageName=<yourstorage>
```

## 3. Configure Key Vault Secrets

```bash
az keyvault secret set --vault-name <your-kv-name> --name "SECRET_KEY" --value "<your-secret>"
az keyvault secret set --vault-name <your-kv-name> --name "JWT_SECRET_KEY" --value "<your-jwt-secret>"
az keyvault secret set --vault-name <your-kv-name> --name "DATABASE_URL" --value "<your-db-url>"
```

## 4. Assign Managed Identity to App Service

- In Azure Portal, enable Managed Identity for your Web App
- Grant Key Vault access policy for "Get" secrets to the Web App's identity

## 5. Configure App Settings for Key Vault References

In the App Service Configuration:
- Add settings like:
  - `SECRET_KEY` = `@Microsoft.KeyVault(SecretUri=https://<your-kv-name>.vault.azure.net/secrets/SECRET_KEY/)`
  - `JWT_SECRET_KEY` = `@Microsoft.KeyVault(SecretUri=https://<your-kv-name>.vault.azure.net/secrets/JWT_SECRET_KEY/)`
  - `DATABASE_URL` = `@Microsoft.KeyVault(SecretUri=https://<your-kv-name>.vault.azure.net/secrets/DATABASE_URL/)`

## 6. Enable Application Insights

- In the App Service Configuration, set `APPINSIGHTS_INSTRUMENTATIONKEY` to the value from your Application Insights resource.

## 7. Deploy via Azure Pipelines (CI/CD)

- Update `azure-pipelines.yml` with your Azure subscription and app name.
- Commit and push to trigger the pipeline.

## 8. Monitor Logs and Metrics

- Use Azure Portal > Application Insights for logs, traces, and metrics.
- Use `az webapp log tail --name <your-app-name> --resource-group <your-rg>` for live logs.

---

For more details, see the official [Azure Web App for Containers documentation](https://learn.microsoft.com/azure/app-service/quickstart-custom-container?tabs=python&pivots=container-linux).
