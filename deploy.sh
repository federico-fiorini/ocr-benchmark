#!/bin/bash

# Update apt-get and install required packages
apt-get update
apt-get install git build-essential python python-dev python-pip libffi-dev libssl-dev websockify

# Install virtualenv
pip install --upgrade pip virtualenv

# Create virtual environments
virtualenv frontend/.env
frontend/.env/bin/pip install -r frontend/requirements.txt

# Run frontend
cd frontend
./run.py