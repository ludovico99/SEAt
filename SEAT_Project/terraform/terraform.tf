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

resource "aws_instance" "SEAt" {
  ami           = "ami-0149b2da6ceec4bb0"   
  instance_type = "t2.medium"
  vpc_security_group_ids = ["sg-0e1f968a157148ba4"]
  key_name = "me-key"
  /*subnet_id              = "subnet-d7c656be"*/
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

output "instance_public_ip" {
  #value =["${aws_instance.SEAt.*.public_ip}"] <-- per piu istanze EC2
  value ="${aws_instance.SEAt.*.public_ip[0]}"
  description = "The public IP address of the main server instance."
}




