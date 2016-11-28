#!/bin/bash

# Update apt-get and install required packages
apt-get update
apt-get install git build-essential python python-dev python-pip libffi-dev libssl-dev websockify

# Install virtualenv
pip install --upgrade pip virtualenv

# Create virtual environments
virtualenv .env
.env/bin/pip install -r requirements.txt

# Run
./run.py