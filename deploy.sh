#!/bin/bash

CURR_PWD=${PWD}
export GOOGLE_APPLICATION_CREDENTIALS="$CURR_PWD/credentials/mcc-2016-g14-p2-c10238f32707.json"

PROJECT_ID="mcc-2016-g14-p2"
PORT=5000

# Set gcloud config
gcloud config set account "mcc.fall.2016.g14@gmail.com"
gcloud config set compute/zone europe-west1-b
gcloud config set project $PROJECT_ID

##### Create mongo replica ######

## Clone mongo sidecar repo
git clone https://github.com/leportlabs/mongo-k8s-sidecar.git
cd mongo-k8s-sidecar/example

# Add 3 replicas
make add-replica DISK_SIZE=200GB ZONE=europe-west1-b ENV=GoogleCloudPlatform
make add-replica DISK_SIZE=200GB ZONE=europe-west1-b ENV=GoogleCloudPlatform
make add-replica DISK_SIZE=200GB ZONE=europe-west1-b ENV=GoogleCloudPlatform

##### Deploy on gcloud with docker and kubernetes ######

# !Make sure to have docker running!
# Build docker image
docker build -t gcr.io/$PROJECT_ID/backend:v1 .

# Push docker image to gcloud
gcloud docker -- push gcr.io/$PROJECT_ID/backend:v1

# Create container
gcloud container clusters create backend
gcloud container clusters get-credentials backend

# Create pod
kubectl run backend -- image=gcr.io/$PROJECT_ID/backend:v1 --port=$PORT

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