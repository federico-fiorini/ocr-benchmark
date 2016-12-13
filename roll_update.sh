#!/bin/bash

# Check if version tag is provided
if [ $# -eq 0 ]
  then
    echo "No version tag provided"
fi

VERSION="$1"

# Make sure to have docker running
CURR_PWD=${PWD}
export GOOGLE_APPLICATION_CREDENTIALS="$CURR_PWD/credentials/google-cloud-auth.json"

PROJECT_ID="ocr-benchmark"
PORT=5000

# Re-build docker image
docker build -t gcr.io/$PROJECT_ID/backend:$VERSION .

# Push it to gcloud
gcloud docker -- push gcr.io/$PROJECT_ID/backend:$VERSION

# Get credentials
gcloud container clusters get-credentials backend

# Update controller image
kubectl set image deployment/backend backend=gcr.io/$PROJECT_ID/backend:$VERSION

sleep 10

EXTERNAL_IP=$(kubectl get services backend | awk '{print $3}' | sed -n 2p)
printf "\n\nFrom your mobile open your browser at https://$EXTERNAL_IP:$PORT \n\n"