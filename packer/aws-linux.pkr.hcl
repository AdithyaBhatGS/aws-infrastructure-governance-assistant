packer {
  required_plugins {
    amazon = {
      source  = "github.com/hashicorp/amazon"
      version = "~> 1.0"
    }
  }
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

source "amazon-ebs" "amazon_linux" {
  ami_name      = "aws-infra-governance-base-{{timestamp}}"
  instance_type = "t3.micro"
  region        = var.aws_region

  source_ami_filter {
    filters = {
      name                = "al2023-ami-2023.*-kernel-*-x86_64"
      root-device-type    = "ebs"
      virtualization-type = "hvm"
    }

    owners      = ["137112412989"]
    most_recent = true
  }

  ssh_username = "ec2-user"
}

build {
  sources = ["source.amazon-ebs.amazon_linux"]

  provisioner "shell" {
    inline = [
      "sudo dnf install -y python3.13 amazon-cloudwatch-agent unzip"
    ]
  }

  post-processor "manifest" {
    output     = "manifest.json"
    strip_path = true
  }
}