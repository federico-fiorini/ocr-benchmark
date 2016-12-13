# ONLINE OCR

Mobile friendly web app to perform OCR.

Local (client side) and Remote (server side) options are available.

Benchmark option compares local and remote performances.

Uses Docker and Kubernetes to deploy a cluster on Google Container Engine.
Uses MongoDB replica set of 3 nodes with persistent disk.
Uses Google Cloud Storage to save source images.


### RESTRICTIONS
Allowed image extensions:

- jpg
- jpeg
- png


Not compatible with Safari.

### INSTRUCTIONS
To run it locally follow these steps:
 
    # Install needed dependencies
    apt-get update --fix-missing
    apt-get install build-essential python python-dev python-pip python-virtualenv libjpeg-dev libffi-dev libssl-dev tesseract-ocr --assume-yes
    
    # Clone the code
    git clone https://github.com/federico-fiorini/ocr-benchmark.git
    cd ocr-benchmark
    
    # Install virtualenv
    pip install --upgrade pip virtualenv
    
    # Install mongodb
    # On Mac
    brew install mongodb
    
    # On Ubuntu
    sudo apt-get install -y mongodb-org
    
    # Run mongodb deamon in a new terminal
    mongod
    
    # Back to previous terminal: create virtual environment
    virtualenv .env
    .env/bin/pip install -r requirements.txt
    
    # Set env variables
    export UPLOAD_FOLDER="/tmp"
    export GOOGLE_APPLICATION_CREDENTIALS="path/to/credentials/google-cloud-auth.json"

    # Run
    ./run.py
    
    # Open the browser at the given IP address


### DEPLOYMENT
To deploy on google cloud follow these steps:

    # 1) Install gcloud and authenticate
    sudo ./install_gcloud.sh
    
    # 2) Run deployment script
    sudo ./deploy.sh
    
    # 3) Open the browser at the given IP address


To roll out an update run:

    # Deploy the last version of the code
    ./roll_update.sh v2


### HOW TO USE IT
Login with one of the following test users:


- username: `user1`, password: `password1`
- username: `user2`, password: `password2`
- username: `user3`, password: `password3`


