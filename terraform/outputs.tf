output "cluster_name" {
  description = "ECS cluster name"
  value       = aws_ecs_cluster.cenconsud2.name
}

output "auth_service_url" {
  description = "Auth service URL"
  value       = "http://${aws_ecs_service.auth_service.load_balancer.0.dns_name}:8001"
}