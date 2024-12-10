resource "azurerm_resource_group" "rg" {
  name     = "${var.resource_group_name}-${random_id.rg_suffix.hex}"
  location = var.location
}

resource "random_id" "rg_suffix" {
  byte_length = 6
}

output "name" {
  value = azurerm_resource_group.rg.name
}
