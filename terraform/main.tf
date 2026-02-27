terraform {
    backend "s3" {
        bucket         = "cali-housing-mlops-tf-state-bro-115"
        key            = "mlops/terraform.tfstate"
        region         = "us-east-1"
        use_lockfile   = true
        encrypt        = true
    }
}

provider "aws" {
    region = "us-east-1"
}

data "aws_ami" "ubuntu" {
    most_recent = true
    owners      = ["099720109477"]
    filter {
        name   = "name"
        values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
    }
}

resource "aws_security_group" "mlops_sg" {
    name        = "mlops_allow_traffic"
    description = "Allow HTTP and SSH"

    ingress {
        from_port   = 5000
        to_port     = 5000
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    ingress {
        from_port   = 22
        to_port     = 22
        protocol    = "tcp"
        cidr_blocks = ["0.0.0.0/0"]
    }

    egress {
        from_port   = 0
        to_port     = 0
        protocol    = "-1"
        cidr_blocks = ["0.0.0.0/0"]
    }
}

resource "aws_instance" "mlops_server" {
    ami                    = data.aws_ami.ubuntu.id
    instance_type          = "t3.micro"
    key_name               = "mlops-key"
    vpc_security_group_ids = [aws_security_group.mlops_sg.id]
    
    user_data = <<-EOF
                #!/bin/bash
                apt-get update -y
                apt-get install docker.io python3-pip git -y
                systemctl start docker
                systemctl enable docker
                usermod -aG docker ubuntu
                EOF
    tags = {
        Name = "CaliHousing-Production-Server"
    }
}

output "server_public_ip" {
    value = aws_instance.mlops_server.public_ip
}