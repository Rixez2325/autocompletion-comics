# IAM role with AmazonEC2RoleforSSM
resource "aws_iam_role" "autocompletion_comics_ec2_role" {
  name = "example_role"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "autocompletion_comics_role" {
  role       = aws_iam_role.autocompletion_comics_ec2_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonEC2RoleforSSM"
}

resource "aws_iam_instance_profile" "autocompletion_comics_profil" {
  name = aws_iam_role.autocompletion_comics_ec2_role.name
  role = aws_iam_role.autocompletion_comics_ec2_role.name
}

# OS of the VM
data "aws_ami" "amazon_linux" {
  most_recent = true
  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*"]
  }
  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
  owners = ["137112412989"] # Amazon
}

resource "aws_instance" "autocompletion_comics_process" {
  ami           = data.aws_ami.amazon_linux.id # "ami-06935448000742e6b"
  instance_type = "p2.xlarge"

  iam_instance_profile = aws_iam_instance_profile.autocompletion_comics_profil.name

  user_data = <<-EOF
                #!/bin/bash
                sudo yum update -y
                sudo yum install amazon-linux-extras
                sudo amazon-linux-extras install epel -y
                sudo yum update -y
                sudo yum install -y git
                sudo yum install git-lfs -y
                sudo yum install python3 -y
                sudo yum install python3-pip -y
                cd /home/ec2-user
                git clone https://github.com/Rixez2325/autocompletion-comics
                cd autocompletion-comics/assets
                git clone https://huggingface.co/ogkalu/Comic-Diffusion
                cd ../
                pip3 install -r python_package/requirements.txt

                EOF

  tags = {
    Name = "comics-generator-process"
  }
}
