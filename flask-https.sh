#!/usr/bin/env bash

# Runs the Flask development server through HTTPS
# using a key pair already signed by our FGI Internal CA
# which is already trusted on developer's work station
#
# See: https://docs.google.com/document/d/1q0H-hEGm5-D-AlQOKgmXNwQGxcjWapAfZXG8O85i2kE/edit

pipenv run flask run \
  --cert=`capath=$(mktemp) && aws s3api get-object --bucket fgi-internal-resources --key localhost-public-key.csr $capath > /dev/null && echo $capath` \
  --key=`capath=$(mktemp) && aws s3api get-object --bucket fgi-internal-resources --key localhost-private-key.key $capath > /dev/null && echo $capath`
