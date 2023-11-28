# Dapr on Azure Container Apps sample

## Running locally
```bash
# Start the order processor service
cd order-processor
export DAPR_STATESTORE_COMPONENT=statestore
export DAPR_PUBSUB_COMPONENT=pubsub
dapr run --app-id order-processor --app-port 6001 -- python3 app.py

# In a separate terminal, start the order publisher service
cd order-publisher
export DAPR_PUBSUB_COMPONENT=pubsub
dapr run --app-id order-publisher -- python3 app.py
```

## Running on ACA

### Pre-requisites (optional)

The images are already present in Microsoft Container Registry, if you are building custom images, you can use the following commands to build and push the images to your own container registry.

```bash
docker buildx build --platform linux/amd64 -t $MY_CONTAINER_REGISTRY/python-order-publisher:latest --push ./order-publisher
docker buildx build --platform linux/amd64 -t $MY_CONTAINER_REGISTRY/python-order-processor:latest --push ./order-processor
```

## Deploying container app environment and apps

```bash
VAR_RESOURCE_GROUP="myResourceGroup"
VAR_ENVIRONMENT="myAcaEnv"
VAR_LOCATION="eastus"

## Create the resource group
az group create \
  --name "$VAR_RESOURCE_GROUP" \
  --location "$VAR_LOCATION"

## Create the managed environment
az deployment group create \
  --resource-group "$VAR_RESOURCE_GROUP" \
  --template-file ./deploy/managedEnvironment.bicep \
  --parameters environment_name="$VAR_ENVIRONMENT" \
  --parameters location="$VAR_LOCATION"

## Initialize Dapr components
az containerapp env dapr-component init -g $VAR_RESOURCE_GROUP --name $VAR_ENVIRONMENT 

## Deploy the container apps
az deployment group create \
  --resource-group "$VAR_RESOURCE_GROUP" \
  --template-file ./deploy/containerApps.bicep \
  --parameters environment_name="$VAR_ENVIRONMENT" \
  --parameters location="$VAR_LOCATION"
```

## Cleanup

```bash
# Delete the resource group
az group delete --name "$VAR_RESOURCE_GROUP"
```