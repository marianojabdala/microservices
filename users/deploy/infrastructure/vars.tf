variable "AWS_ACCESS_KEY" {}
variable "AWS_SECRET_KEY" {}
variable "AWS_REGION" {
  default = "us-east-1"
}
variable "AMIS" {
  type = "map"
  default = {
    us-east-1 = "ami-43a15f3e"
  }
}

variable "PATH_TO_PRIVATE_KEY" {
  default = "my-ssh-key"
}
variable "PATH_TO_PUBLIC_KEY" {
  default = "my-ssh-key.pub"
}
