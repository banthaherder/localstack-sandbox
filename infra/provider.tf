provider "aws" {
  region = "us-east-1"
  
  # for tflocal testing via localstack
  skip_requesting_account_id = true
}
