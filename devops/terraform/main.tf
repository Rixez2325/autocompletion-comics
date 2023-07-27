provider "aws" {
  region = "eu-west-1"
}

data "aws_s3_bucket" "existing" {
  bucket = "autocompletion-comics-buckets"
}

data "aws_iam_user" "existing_user" {
  user_name = "codecommit_user"
}
