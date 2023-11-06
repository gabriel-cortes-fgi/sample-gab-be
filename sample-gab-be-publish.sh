#!/usr/bin/env bash

# Builds and pushes the docker image to our private AWS ECR
#
# Useful in development, where you want to skip the GitHub actions temporarily
#
# Source: https://docs.aws.amazon.com/AmazonECR/latest/userguide/getting-started-cli.html

APP_NAME=service-test

docker build -t $APP_NAME --platform=linux/amd64 --build-arg PIPENV_PYPI_MIRROR=$(pip3 config get global.index-url) -f sample-gab-be.dockerfile . \
&& docker tag $APP_NAME:latest 534468236225.dkr.ecr.ap-southeast-1.amazonaws.com/$APP_NAME:latest \
&& docker push 534468236225.dkr.ecr.ap-southeast-1.amazonaws.com/$APP_NAME:latest
