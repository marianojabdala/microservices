## Deploy the users microservice in AWS

#### Requirements
 - AWS account
 - Terraform
 - Public and private key (see -Notes)

## Instructions

Execute

    terraform init

This will download all the provisiones that will be used.

Then execute

    terraform apply

In case the we do not want to push the changes directly to AWS, we could use

    terraform plan -out plan

to see what terraform will do and then

    terraform apply plan

to create the infrastructure.

## Login

To enter the new EC2 instance just login with:

      ssh -i my-ssh-key -l ubuntu [output-ip]

## Notes

To generate the public and private key to be able to ssh to the instance run this command:

      ssh-keygen -f my-ssh-key

leave the password blank, so just press enter.
