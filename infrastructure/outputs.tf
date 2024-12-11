output "private_endpoint_ip" {
  value = module.backend_app.database_private_ip
}

output "sql_connection_string" {
  value = "mssql+pyodbc:///?odbc_connect=Driver={ODBC Driver 18 for SQL Server};Server=tcp:${azurerm_mssql_server.server.fully_qualified_domain_name},1433;Database=userdb;Uid=adminuser;Pwd={P@ssword123};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
}
output "app_name" {
  value = module.backend_app.app_name
}