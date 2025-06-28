param location string = 'eastus'
param appServicePlanSku string = 'B1'
param pythonVersion string = '3.11'

resource appServicePlan 'Microsoft.Web/serverfarms@2022-03-01' = {
  name: 'fragranceAppPlan'
  location: location
  sku: {
    name: appServicePlanSku
    tier: 'Basic'
  }
}

resource webApp 'Microsoft.Web/sites@2022-03-01' = {
  name: 'fragrance-guess-app-${uniqueString(resourceGroup().id)}'
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
