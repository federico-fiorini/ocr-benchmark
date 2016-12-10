FROM ubuntu:14.04

# no tty
ENV DEBIAN_FRONTEND noninteractive
ENV MONGODB_HOST mongodb://mongo-1,mongo-2,mongo-3:27017
ENV UPLOAD_FOLDER /images

# get up to date
RUN apt-get -qq update --fix-missing

# Bootstrap the image so that it includes all of our dependencies
RUN apt-get -qq install build-essential python python-dev python-pip \
python-virtualenv libjpeg-dev libffi-dev libssl-dev tesseract-ocr cron --assume-yes

# Add crontab file in the cron directory
ADD crontab /etc/cron.d/delete-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/delete-cron

# Copy to /app
COPY . /app
WORKDIR /app

RUN mkdir -p /images/

# Create a virtualenv
RUN mkdir -p /.env/
RUN virtualenv /.env/

# Install python dependencies in virtualenv
RUN /.env/bin/pip install -r /app/requirements.txt

# Expose a port for the flask development server
EXPOSE 5000

# Run cron
CMD cron

# Run flask app
CMD ["/.env/bin/python", "/app/run.py"]
