variable "app_name" {}
variable "resource_group_name" {}
variable "location" {}
variable "app_service_plan_name" {}
variable "virtual_network_subnet_id" {}
variable "database_private_ip" {
  description = "The private IP of the database's private endpoint"
  type        = string
}
