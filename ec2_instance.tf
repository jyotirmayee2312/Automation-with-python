provider "aws" {
  region = "ap-south-1"
}

resource "aws_instance" "ec2_instance" {
  ami           = "ami-0da59f1af71ea4ad2"
  instance_type = "t2.micro"
  key_name      = "aws_login"
}

