output "instance" {
  value = "${aws_instance.users.public_ip}"
}
