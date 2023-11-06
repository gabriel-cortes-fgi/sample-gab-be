#!/usr/bin/env bash

if ! [ -x "$(command -v aws)" ]; then
  if [[ $(uname -m) == arm* ]]; then
    echo "Downloading aws-cli for ARM"
    curl "https://awscli.amazonaws.com/awscli-exe-linux-aarch64.zip" -o "awscliv2.zip" #> /dev/null 2>&1
    echo "Unzipping awscliv2.zip"
    unzip awscliv2.zip #> /dev/null 2>&1
    echo "Installing aws-cli"
    ./aws/install #> /dev/null 2>&1
  else
    echo "Downloading aws-cli for x86"
    curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" #> /dev/null 2>&1
    echo "Unzipping awscliv2.zip"
    unzip awscliv2.zip #> /dev/null 2>&1
    echo "Installing aws-cli"
    ./aws/install #> /dev/null 2>&1
  fi
else
    echo "aws-cli is already installed"
fi

echo "Logging in pip..."
aws codeartifact login --tool pip --repository pypi --domain fgi --domain-owner 534468236225 --region ap-southeast-1
echo ""