#!/bin/bash

##### Deploy on gcloud with docker and kubernetes ######

# Make sure to have docker running
CURR_PWD=${PWD}
export GOOGLE_APPLICATION_CREDENTIALS="$CURR_PWD/credentials/mcc-2016-g14-p2-c10238f32707.json"

PROJECT_ID="mcc-2016-g14-p2"
PORT=5000

# Build docker image
docker build -t gcr.io/$PROJECT_ID/backend:v1 .

# Push docker image to gcloud
gcloud docker -- push gcr.io/$PROJECT_ID/backend:v1

# Set gcloud config
gcloud config set account "mcc.fall.2016.g14@gmail.com"
gcloud config set compute/zone europe-west1-b
gcloud config set project $PROJECT_ID

# Create container
gcloud container clusters create backend
gcloud container clusters get-credentials backend

# Create pod
kubectl run backend --image=gcr.io/$PROJECT_ID/backend:v1 --port=$PORT

# Create service
kubectl expose deployment backend --type="LoadBalancer"

printf "\n\nWaiting for IP... "

# Get external IP
while true; do

    EXTERNAL_IP=$(kubectl get services backend | awk '{print $3}' | sed -n 2p)
    if [[ $EXTERNAL_IP =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
        break
    fi

    sleep 2
    echo -ne "#"
done

printf "\n\nFrom your mobile open your browser at https://$EXTERNAL_IP:$PORT \n\n"