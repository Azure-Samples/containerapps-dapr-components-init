param environment_name string
param location string

resource environment 'Microsoft.App/managedEnvironments@2022-03-01' existing = {
  name: environment_name
}

resource orderPublisher 'Microsoft.App/containerApps@2023-05-01' = {
  name: 'order-publisher'
  location: location
  properties: {
    managedEnvironmentId: environment.id
    configuration: {
      dapr: {
        enabled: true
        appId: 'order-publisher'
        appProtocol: 'http'
        enableApiLogging: false
      }
    }
    template: {
      containers: [
        {
          image: 'daprms.azurecr.io/public/daprio/samples/azcli-capps/python-order-publisher:latest'
          name: 'order-publisher'
          env: [
            {
              name: 'DAPR_PUBSUB_COMPONENT'
              value: 'pubsub'
            }
          ]
          resources: {
            cpu: json('0.5')
            memory: '1.0Gi'
          }
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 1
      }
    }
  }
}

resource orderProcessor 'Microsoft.App/containerApps@2023-05-01' = {
  name: 'order-processor'
  location: location
  properties: {
    managedEnvironmentId: environment.id
    configuration: {
      dapr: {
        enabled: true
        appId: 'order-processor'
        appProtocol: 'http'
        appPort: 8080
        enableApiLogging: false
      }
    }
    template: {
      containers: [
        {
          image: 'daprms.azurecr.io/public/daprio/samples/azcli-capps/python-order-processor:latest'
          name: 'order-processor'
          env: [
            {
              name: 'DAPR_PUBSUB_COMPONENT'
              value: 'pubsub'
            }
            {
              name: 'DAPR_STATESTORE_COMPONENT'
              value: 'statestore'
            }
            {
              name: 'APP_PORT'
              value: '8080'
            }
          ]
          resources: {
            cpu: json('0.5')
            memory: '1.0Gi'
          }
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 1
      }
    }
  }
}
