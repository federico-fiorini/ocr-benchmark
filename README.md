# ONLINE OCR

Mobile friendly web app to perform OCR

### INSTRUCTIONS
To run it locally follow these steps:
 
    # Clone the code
    git clone git@git.niksula.hut.fi:cs-e4100/mcc-2016-g14-p2.git
    cd mcc-2016-g14-p2
    
    # Install virtualenv
    pip install --upgrade pip virtualenv
    
    # Install mongodb
    # On Mac
    brew install mongodb
    
    # On Ubuntu
    sudo apt-get install -y mongodb-org
    
    # Run mongodb deamon in a new terminal
    mongod
    
    # Back to the first terminal: create database and import test users
    mongorestore -d remote_ocr mongo/remote_ocr
    
    # Create virtual environment
    virtualenv .env
    .env/bin/pip install -r requirements.txt
    
    # Set env variables
    export UPLOAD_FOLDER="/tmp"

    # Run
    ./run.py
   
### DEPLOYMENT
To deploy on google cloud follow these steps:

    # 1) Run Docker client
    
    # 2) Run deployment script
    ./deploy.sh


To roll out an update run:

    # Deploy the last version of the code
    ./roll_update.sh
