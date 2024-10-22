#!/bin/bash
# This script use to just be the following two lines...
# cd site-deploy
# s3cmd sync .  s3://www.haydnenthusiasts.org/ --acl-public
# aws s3 sync . s3://www.haydnenthusiasts.org/ --acl public-read

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

deploy_with_s3cmd() {
    echo "Deploying with s3cmd..."
    s3cmd sync . s3://www.haydnenthusiasts.org/ --acl-public
    return $?
}

deploy_with_aws() {
    echo "Deploying with AWS CLI..."
    aws s3 sync . s3://www.haydnenthusiasts.org/ --acl public-read
    return $?
}

# Main logic
cd site-deploy
if command_exists s3cmd; then
    deploy_with_s3cmd
elif command_exists aws; then
    deploy_with_aws
else
    echo "Error: Neither s3cmd nor aws CLI is installed."
    echo "Please install either s3cmd or AWS CLI to continue."
    exit 1
fi

# Check if deployment was successful
if [ $? -eq 0 ]; then
    echo "Deployment completed successfully!"
else
    echo "Deployment failed with error code $?"
    exit 1
fi