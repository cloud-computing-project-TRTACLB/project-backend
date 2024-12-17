  # Création du serveur SQL
  resource "azurerm_mssql_server" "server" {
    name                        = "${var.database_name}-${random_id.db_suffix.hex}"
    resource_group_name         = var.resource_group_name
    location                    = var.location
    version                     = "12.0"  # Exemple de version (à ajuster selon vos besoins)
    administrator_login         = var.admin_user
    administrator_login_password = var.admin_password
  }
  # Autoriser les services Azure à accéder au serveur SQL
resource "azurerm_mssql_firewall_rule" "allow_azure_services" {
  name                = "AllowAzureServices"
  server_id           = azurerm_mssql_server.server.id
  start_ip_address    = "0.0.0.0"
  end_ip_address      = "0.0.0.0"
}
  # Génération d'un suffixe aléatoire pour nommer la base de données
  resource "random_id" "db_suffix" {
    byte_length = 6
  }

  # Création de la base de données
  resource "azurerm_mssql_database" "db" {
    name      = var.database_name
    server_id = azurerm_mssql_server.server.id
  }

  # Création du Private Endpoint
  resource "azurerm_private_endpoint" "db_private_endpoint" {
    name                = "db-private-endpoint-${random_id.rule_suffix.hex}"
    location            = var.location
    resource_group_name = var.resource_group_name
    subnet_id           = var.subnet_id  # Utilisation de la variable pour le subnet ID

    private_service_connection {
      name                           = "sql-private-connection"
      private_connection_resource_id = azurerm_mssql_server.server.id
      subresource_names              = ["sqlServer"]
      is_manual_connection           = false  # Connexion automatique
    }
  }

  # Génération d'un suffixe pour le Private Endpoint
  resource "random_id" "rule_suffix" { 
    byte_length = 6
  }

