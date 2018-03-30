resource "aws_key_pair" "my-ssh-key" {
  key_name = "my-ssh-key"
  public_key = "${file("${var.PUBLIC_KEY}")}"
}

resource "aws_instance" "users" {
  ami           = "${lookup(var.AMIS, var.AWS_REGION)}"
  instance_type = "t2.micro"
  key_name = "${aws_key_pair.my-ssh-key.key_name}"

  # the VPC subnet
  subnet_id = "${aws_subnet.main-public.id}"

  # the security group
  vpc_security_group_ids = ["${aws_security_group.allow-ssh.id}",
    "${aws_security_group.allow-http.id}"]

  # user data
  user_data = "${data.template_cloudinit_config.cloudinit-users.rendered}"

  tags {
     Name = "users-service"
   }

  connection {
    user = "${var.INSTANCE_USERNAME}"
    private_key = "${file("${var.PRIVATE_KEY}")}"
  }
}
