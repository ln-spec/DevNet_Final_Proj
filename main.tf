provider "aws" {
  region                      = var.aws_region
  skip_credentials_validation = true
  skip_requesting_account_id  = true
  skip_metadata_api_check     = true

  # Redirects requests away from real AWS servers
  endpoints {
    sts = "http://localhost:4566"
    ec2 = "http://localhost:4566"
  }
}

locals {
  # Hardcoded static AZs instead of data source lookup to prevent terminal hanging
  azs             = ["${var.aws_region}a", "${var.aws_region}b"]
  public_cidrs    = [for i in range(2) : cidrsubnet(var.vpc_cidr, 8, i)]
  private_cidrs   = [for i in range(2) : cidrsubnet(var.vpc_cidr, 8, i + 10)]
  nat_az_indices  = var.nat_strategy == "per_az" ? [0, 1] : [0]
  common_tags     = { Project = "San-Rafael-E-Government", Environment = "disaster-recovery", ManagedBy = "Terraform" }
}

resource "aws_vpc" "main" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags                 = merge(local.common_tags, { Name = "${var.name_prefix}-vpc" })
}

resource "aws_internet_gateway" "main" {
  vpc_id = aws_vpc.main.id
  tags   = merge(local.common_tags, { Name = "${var.name_prefix}-igw" })
}

resource "aws_subnet" "public" {
  count                   = 2
  vpc_id                  = aws_vpc.main.id
  availability_zone       = local.azs[count.index]
  cidr_block              = local.public_cidrs[count.index]
  map_public_ip_on_launch = true
  tags                    = merge(local.common_tags, { Name = "${var.name_prefix}-public-${count.index + 1}" })
}

resource "aws_subnet" "private" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  availability_zone = local.azs[count.index]
  cidr_block        = local.private_cidrs[count.index]
  tags              = merge(local.common_tags, { Name = "${var.name_prefix}-private-${count.index + 1}" })
}

resource "aws_eip" "nat" {
  count  = length(local.nat_az_indices)
  domain = "vpc"
  tags   = merge(local.common_tags, { Name = "${var.name_prefix}-nat-eip-${count.index + 1}" })
}

resource "aws_nat_gateway" "main" {
  count         = length(local.nat_az_indices)
  allocation_id = aws_eip.nat[count.index].id
  subnet_id     = aws_subnet.public[local.nat_az_indices[count.index]].id
  depends_on    = [aws_internet_gateway.main]
  tags          = merge(local.common_tags, { Name = "${var.name_prefix}-nat-${count.index + 1}" })
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.main.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.main.id
  }
  tags = merge(local.common_tags, { Name = "${var.name_prefix}-public-rt" })
}

resource "aws_route_table_association" "public" {
  count          = 2
  subnet_id      = aws_subnet.public[count.index].id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table" "private" {
  count  = 2
  vpc_id = aws_vpc.main.id
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.main[var.nat_strategy == "per_az" ? count.index : 0].id
  }
  tags = merge(local.common_tags, { Name = "${var.name_prefix}-private-rt-${count.index + 1}" })
}

resource "aws_route_table_association" "private" {
  count          = 2
  subnet_id      = aws_subnet.private[count.index].id
  route_table_id = aws_route_table.private[count.index].id
}

resource "aws_security_group" "web" {
  name        = "${var.name_prefix}-web"
  description = "Public HTTP and HTTPS access to the portal only."
  vpc_id      = aws_vpc.main.id
  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  ingress {
    description = "HTTPS"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = merge(local.common_tags, { Name = "${var.name_prefix}-web-sg" })
}

resource "aws_instance" "portal" {
  # Static placeholder ID to prevent dynamic AMI query hangs
  ami                         = "ami-mockid12345678"
  instance_type               = var.instance_type
  subnet_id                   = aws_subnet.public[0].id
  vpc_security_group_ids      = [aws_security_group.web.id]
  associate_public_ip_address = true
  user_data_replace_on_change = true
  user_data = <<-EOF
    #!/bin/bash
    set -euxo pipefail
    dnf install -y nginx
    cat > /usr/share/nginx/html/index.html <<'HTML'
    <!doctype html><html lang="en"><meta charset="utf-8"><title>San Rafael Disaster Alert Portal</title><h1>San Rafael Disaster Alert Portal</h1><p>DR placeholder service is online. Official alerts and municipal services will appear here.</p><p>This demonstration page is not an emergency alert channel.</p></html>
    HTML
    systemctl enable --now nginx
  EOF
  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
  }
  root_block_device {
    encrypted   = true
    volume_type = "gp3"
    volume_size = 8
  }
  tags = merge(local.common_tags, { Name = "${var.name_prefix}-portal" })
}
