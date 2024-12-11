output "app_name"{
    value = module.backend_app.app_name
}

output "private_endpoint_ip"{
    value = module.database_user.private_endpoint_ip
}

output "sql_connection_string"{
    value = module.database_user.sql_connection_string
}

output "publish_profile"{
    value = "https://${module.backend_app.app_name}.azurewebsites.net"
}