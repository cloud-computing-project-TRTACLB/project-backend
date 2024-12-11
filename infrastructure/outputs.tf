output "app_name"{
    value = module.backend_app.app_name
}

output "private_endpoint_ip"{
    value = module.database.private_endpoint_ip
}

output "sql_connection_string"{
    value = module.database.sql_connection_string
}