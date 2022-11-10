terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
    }
  }
}

provider "aws" {
  profile = "default"
  region  = "us-east-1"
  shared_credentials_files = ["$HOME/.aws/credentials"]
}
variable "ami" {}
variable "security_group"{}
variable "instance_type" {}
variable "key_name"{}


resource "aws_instance" "SEAt" {
  ami           = var.ami
  instance_type = var.instance_type
  vpc_security_group_ids = [var.security_group]
  key_name = var.key_name
  tags = {
    Name = "SEAt"
  }
}

data "external" "get_table" {
  program = ["python3","createDynamoDbTables.py"]

}

output "tables" {
  value = data.external.get_table.result
}

data "external" "get_queue" {
  program = ["python3","createQueue.py"]
}

output "queue" {
  value = data.external.get_queue.result
  
}

output "instance_public_ip" {
  #value =["${aws_instance.SEAt.*.public_ip}"] <-- per piu istanze EC2
  value ="${aws_instance.SEAt.*.public_ip[0]}"
  description = "The public IP address of the main server instance."
}




