FROM ubuntu:14.04

# no tty
ENV DEBIAN_FRONTEND noninteractive
ENV MONGODB_HOST mongodb://mongo-1,mongo-2,mongo-3:27017
ENV UPLOAD_FOLDER /images

# get up to date
RUN apt-get -qq update --fix-missing

# Bootstrap the image so that it includes all of our dependencies
RUN apt-get -qq install build-essential python python-dev python-pip python-virtualenv libjpeg-dev libffi-dev libssl-dev tesseract-ocr rabbitmq-server --assume-yes

# Run rabbitmq-server
RUN rabbitmq-server &

COPY . /app
WORKDIR /app

RUN mkdir -p /images/

# create a virtualenv we can later use
RUN mkdir -p /.env/
RUN virtualenv /.env/

# install python dependencies from pypi into venv
RUN /.env/bin/pip install -r /app/requirements.txt

# Run celery deamon
RUN /.env/bin/celery worker -A app.celery_app -B &

# expose a port for the flask development server
EXPOSE 5000

# run our flask app inside the container
CMD ["/.env/bin/python", "/app/run.py"]
