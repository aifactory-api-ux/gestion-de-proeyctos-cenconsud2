terraform {
  required_version = ">= 1.6"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}

resource "aws_ecs_cluster" "cenconsud2" {
  name = "cenconsud2-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}

resource "aws_ecs_task_definition" "auth_service" {
  family = "auth-service"

  container_definitions = jsonencode([{
    name      = "auth-service"
    image     = "${var.ecr_repository_url}/auth-service:latest"
    essential = true
    portMappings = [{
      containerPort = 8001
      protocol      = "tcp"
    }]
    environment = [
      { name = "POSTGRES_HOST", value = var.postgres_host },
      { name = "POSTGRES_PORT", value = var.postgres_port },
      { name = "POSTGRES_DB", value = var.postgres_db },
      { name = "POSTGRES_USER", value = var.postgres_user },
      { name = "POSTGRES_PASSWORD", value = var.postgres_password },
      { name = "REDIS_HOST", value = var.redis_host },
      { name = "REDIS_PORT", value = var.redis_port },
      { name = "JWT_SECRET", value = var.jwt_secret },
      { name = "LOG_LEVEL", value = "INFO" }
    ]
  }])
}

resource "aws_ecs_service" "auth_service" {
  name            = "auth-service"
  cluster         = aws_ecs_cluster.cenconsud2.name
  task_definition = aws_ecs_task_definition.auth_service.arn
  desired_count    = 2

  load_balancer {
    target_group_arn = aws_lb_target_group.auth.arn
    container_name   = "auth-service"
    container_port   = 8001
  }
}