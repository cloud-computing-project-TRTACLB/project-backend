terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.75"
    }
  }
}

provider "azurerm" {
  features {}
}


module "resource_group" {
  source = "./modules/ressource_group"
  resource_group_name = "Cloud-computing-project"
  location            = var.location
}
  
module "virtual_network" {
  source              = "./modules/virtual_network"
  resource_group_name = module.resource_group.name
  location            = var.location
  vnet_name           = "vnet-10-0-0-0-16"
  address_space       = "10.0.0.0/16"
}


      
module "backend_app" {
  source                  = "./modules/backend"
  app_name                = "backend-app"
  app_service_plan_name   = "example"
  resource_group_name     = module.resource_group.name
  location                = var.location
  virtual_network_subnet_id = module.virtual_network.subnets[0]
  database_private_ip = module.database_user.private_endpoint_ip  # Passer l'IP privée du module database
}

module "database_user" {
  source              = "./modules/database"
  database_name       = "userdb"
  resource_group_name = module.resource_group.name
  location            = var.location
  admin_user          = "adminuser"
  admin_password      = "P@ssword123"
  subnet_id           = module.virtual_network.subnets[1]  # ID du subnet 'database-subnet' 
}

module "database_items" {
  source              = "./modules/database"
  database_name       = "itemsdb"
  resource_group_name = module.resource_group.name
  location            = var.location
  admin_user          = "adminuser"
  admin_password      = "P@ssword123"
  subnet_id           = module.virtual_network.subnets[1]  # ID du subnet 'database-subnet'
}


