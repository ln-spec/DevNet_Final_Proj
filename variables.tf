terraform {
  required_version = ">= 1.5.0, < 2.0.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

variable "aws_region" {
  description = "AWS region for disaster recovery resources."
  type        = string
  default     = "ap-southeast-1"
}

variable "vpc_cidr" {
  description = "IPv4 CIDR block for the VPC."
  type        = string
  default     = "10.40.0.0/16"
}

variable "instance_type" {
  description = "EC2 instance type for the placeholder portal."
  type        = string
  default     = "t3.micro"
}

variable "nat_strategy" {
  description = "Use one cost-saving NAT gateway or one NAT gateway per AZ."
  type        = string
  default     = "single"
  validation {
    condition     = contains(["single", "per_az"], var.nat_strategy)
    error_message = "nat_strategy must be single or per_az."
  }
}

variable "localstack_enabled" {
  description = "Configure AWS provider endpoints and path-style S3 access for LocalStack."
  type        = bool
  default     = false
}

variable "localstack_endpoint" {
  description = "Base endpoint for LocalStack services."
  type        = string
  default     = "http://localhost:4566"
}

variable "name_prefix" {
  description = "Prefix applied to resource names and tags."
  type        = string
  default     = "san-rafael-dr"
}
