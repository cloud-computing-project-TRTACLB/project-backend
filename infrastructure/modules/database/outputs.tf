  # Récupération de l'adresse IP privée du Private Endpoint

output "private_endpoint_ip" {
  value = azurerm_private_endpoint.db_private_endpoint.private_service_connection[0].private_ip_address
}

output "sql_connection_string" {
  value = "jdbc:sqlserver://${azurerm_mssql_server.server.fully_qualified_domain_name};database=${azurerm_mssql_database.db.name};user=${var.admin_user};password=${var.admin_password};"

}
