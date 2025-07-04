param location string = 'southcentralus'
param appServicePlanSku string = 'B1'
param pythonVersion string = '3.11'

resource appServicePlan 'Microsoft.Web/serverfarms@2024-11-01' = {
  name: 'sensoryAppPlan'
  location: location
  kind: 'linux'
  sku: {
    name: appServicePlanSku
    tier: 'Basic'
  }
  properties: {
    reserved: true
  }
}

resource webApp 'Microsoft.Web/sites@2024-04-01' = {
  name: 'sensory-evaluation-quiz-${uniqueString(resourceGroup().id)}'
  kind: 'app,linux'
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: 'PYTHON|${pythonVersion}'
      alwaysOn: true
    }
    httpsOnly: true
  }
}

output webAppUrl string = 'https://${webApp.properties.defaultHostName}'
