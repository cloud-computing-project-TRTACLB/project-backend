  # Récupération de l'adresse IP privée du Private Endpoint

output "private_endpoint_ip" {
  value = azurerm_private_endpoint.db_private_endpoint.private_service_connection.private_ip_address
}

output "sql_connection_string" {
  value = "mssql+pyodbc:///?odbc_connect=Driver={ODBC Driver 18 for SQL Server};Server=tcp:${azurerm_mssql_server.server.fully_qualified_domain_name},1433;Database=userdb;Uid=adminuser;Pwd={P@ssword123};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
}
