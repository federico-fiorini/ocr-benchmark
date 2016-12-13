#!/bin/bash

# Install dependencies
sudo apt-get install make kubectl docker.io

# Start docker deamon
sudo service docker start

# Ser variables
CURR_PWD=${PWD}
export GOOGLE_APPLICATION_CREDENTIALS="$CURR_PWD/credentials/google-cloud-auth.json"

PROJECT_ID="ocr-benchmark"
PORT=5000

# Set gcloud config
gcloud config set account "account@gmail.com"
gcloud config set compute/zone europe-west1-b
gcloud config set project $PROJECT_ID

# !Make sure to have docker running!
# Build docker image
docker build -t gcr.io/$PROJECT_ID/backend:v1 .

# Push docker image to gcloud
gcloud docker -- push gcr.io/$PROJECT_ID/backend:v1

# Create container cluster
gcloud container clusters create backend --num-nodes=3
gcloud container clusters get-credentials backend


##### Create mongo replica ######

# Clone mongo sidecar repo
git clone https://github.com/leportlabs/mongo-k8s-sidecar.git
cd mongo-k8s-sidecar/example

# Add 3 replicas
make add-replica DISK_SIZE=200GB ZONE=europe-west1-b ENV=GoogleCloudPlatform
make add-replica DISK_SIZE=200GB ZONE=europe-west1-b ENV=GoogleCloudPlatform
make add-replica DISK_SIZE=200GB ZONE=europe-west1-b ENV=GoogleCloudPlatform

printf "\n\nWaiting for mongo replica to elect master\n"
sleep 10


##### Create Cloud Storage bucket ######

gsutil mb -p $PROJECT_ID -l EU gs://$PROJECT_ID/
gsutil defacl set public-read gs://$PROJECT_ID

##### Run kubernetes service ######

# Create pod
kubectl run backend --image=gcr.io/$PROJECT_ID/backend:v1 --port=$PORT --replicas=5

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

# Wait some more seconds
sleep 10

printf "\n\nFrom your mobile open your browser at https://$EXTERNAL_IP:$PORT \n\n"