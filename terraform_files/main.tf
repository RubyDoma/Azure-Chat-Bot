terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.8"
    }
  }
  backend "azurerm" {
    resource_group_name  = "AtlassianRG"
    storage_account_name = "atlassiansa"
    container_name       = "tfstate"
    key                  = "terraform.tfstate"
  }
}

provider "azurerm" {
  subscription_id = var.subscription_id
  tenant_id       = var.tenantid
  client_id       = var.clientid
  features {}
}


data "azurerm_resource_group" "main" {
  name = "AtlassianRG"

}

data "azurerm_storage_account" "AtlassianSA" {
  name                = "atlassiansa"
  resource_group_name = data.azurerm_resource_group.main.name

}

data "azurerm_storage_container" "tfstate" {
  name                 = "tfstate"
  storage_account_name = data.azurerm_storage_account.AtlassianSA.name

}


resource "azurerm_service_plan" "main" {
  name                = "terraformed-asp"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  os_type             = "Linux"
  sku_name            = "B1" # allows more config settings

}

data "azurerm_client_config" "current" {}


resource "azurerm_windows_web_app" "main" {
  location            = data.azurerm_resource_group.main.location
  name                = "atlassian-chat"
  resource_group_name = data.azurerm_resource_group.main.name
  https_only          = true
  service_plan_id     = azurerm_service_plan.main.id
  site_config {
    app_command_line = "pip install -r requirements.txt && gunicorn --bind 0.0.0.0 --worker-class aiohttp.worker.GunicornWebWorker --timeout 600 app:APP"
    always_on        = false
   
    # python_version = "3.8" 
    # this setting has been deprecated for windows web apps.                                      
  }

  app_settings = {
    "MicrosoftAppType"                         = "MultiTenant"
    "MicrosoftAppId"                           = data.azurerm_client_config.current.client_id
    "MicrosoftAppPassword"                     = var.clientsecret
    SCM_DO_BUILD_DURING_DEPLOYMENT             = true
    ENABLE_ORYX_BUILD                          = false
  }
}

resource "azurerm_bot_web_app" "AtlassianChat" {
  name                = "AtlassianChat"
  location            = "global"
  resource_group_name = data.azurerm_resource_group.main.name
  sku                 = "F0"
  microsoft_app_id    = data.azurerm_client_config.current.client_id
  endpoint            = "https://atlassian-chat.azurewebsites.net/api/messages"
}


resource "azurerm_bot_channel_ms_teams" "Atlassian" {
  bot_name            = azurerm_bot_web_app.AtlassianChat.name
  location            = "global"
  resource_group_name = data.azurerm_resource_group.main.name

}


resource "azurerm_monitor_action_group" "main" {
  name                = "atlassianactiongroup"
  resource_group_name = data.azurerm_resource_group.main.name
  short_name          = "aag"

  email_receiver {
    name          = "Ruby Domanico"
    email_address = "ruby.domanico@kpmg.co.uk"
  }
}
resource "azurerm_monitor_metric_alert" "cpu-alert" {
  #provider            = azurerm.cs
  name                = "Atlassian-chat-bot-CUP-usage-alert"
  resource_group_name = data.azurerm_resource_group.main.name
  scopes              = [azurerm_service_plan.main.id]
  description         = "We are alerting you because there is a spike in %CPU usage."
  severity            = "2"
  frequency           = "PT5M"
  auto_mitigate       = true
  enabled             = true

  criteria {
    metric_namespace = "Microsoft.Web/serverfarms"
    metric_name      = "CpuPercentage"
    aggregation      = "Average"
    operator         = "GreaterThan"
    threshold        = 80
  }
  action {
    action_group_id = azurerm_monitor_action_group.main.id
  }
}
