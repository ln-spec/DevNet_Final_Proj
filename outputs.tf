output "portal_public_ip" {
  description = "Public IPv4 address of the Disaster Alert Portal EC2 instance."
  value       = aws_instance.portal.public_ip
}

output "portal_public_dns" {
  description = "Public DNS name of the Disaster Alert Portal EC2 instance."
  value       = aws_instance.portal.public_dns
}

output "vpc_id" {
  description = "ID of the disaster recovery VPC."
  value       = aws_vpc.main.id
}
