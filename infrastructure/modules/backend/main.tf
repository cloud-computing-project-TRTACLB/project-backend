resource "azurerm_service_plan" "example" {
  name                = var.app_service_plan_name
  resource_group_name = var.resource_group_name
  location            = var.location
  os_type             = "Linux"
  sku_name            = "B1"
}

resource "azurerm_linux_web_app" "app" {
  name                = "${var.app_name}-${random_id.app_suffix.hex}"
  resource_group_name = var.resource_group_name
  location            = var.location
  service_plan_id     = azurerm_service_plan.example.id

  site_config {

    always_on = false
  }
  virtual_network_subnet_id = var.virtual_network_subnet_id

  app_settings = {
    "DATABASE_URL" = "mssql+pyodbc:///?odbc_connect=Driver={ODBC Driver 18 for SQL Server};Server=tcp:${azurerm_mssql_server.server.fully_qualified_domain_name},1433;Database=userdb;Uid=adminuser;Pwd={P@ssword123};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
  }
}

resource "random_id" "app_suffix" {
  byte_length = 6
}
output "app_name" {
  value = azurerm_linux_web_app.app.name
}