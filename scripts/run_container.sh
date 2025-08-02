##!/bin/bash
#
## Go to app directory
#cd /home/ec2-user/app
#
## Stop and remove old container
#docker stop myapp || true
#docker rm myapp || true
#
## Pull latest image from ECR (make sure you’re authenticated)
#aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 767397763254.dkr.ecr.ap-south-1.amazonaws.com
#
## Run latest image
#docker run -d --name myapp -p 80:80 public.ecr.aws/e1j8m7p9/thamanyah-repo:latest