#!/bin/bash

# Make sure to have docker running
CURR_PWD=${PWD}
export GOOGLE_APPLICATION_CREDENTIALS="$CURR_PWD/credentials/mcc-2016-g14-p2-c10238f32707.json"

PROJECT_ID="mcc-2016-g14-p2"
PORT=5000

# Re-build docker image
docker build -t gcr.io/$PROJECT_ID/backend:v1 .

# Push it to gcloud
gcloud docker -- push gcr.io/$PROJECT_ID/backend:v1

# Update controller image
kubectl set image deployment/backend backend=gcr.io/$PROJECT_ID/backend:v1

EXTERNAL_IP=$(kubectl get services backend | awk '{print $3}' | sed -n 2p)
printf "\n\nFrom your mobile open your browser at https://$EXTERNAL_IP:$PORT \n\n"