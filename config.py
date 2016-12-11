import os

UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', '/tmp')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

SECRET_KEY = os.environ.get('SECRET_KEY', 'development key')
SALT = 'fV3Q26FcTz2DsHFf'

SESSION_TYPE = os.environ.get('SESSION_TYPE', 'filesystem')

# Mongo connection
MONGODB_HOST = os.environ.get('MONGODB_HOST', 'localhost')
MONGODB_DB = os.environ.get('MONGODB_DB', 'remote_ocr')

# Test users file
TEST_USERS = os.environ.get('TEST_USERS', 'users.json')

SOURCE_IMAGE_LIFETIME = os.environ.get('SOURCE_IMAGE_LIFETIME', '7')

GOOGLE_BUCKET_NAME = os.environ.get('GOOGLE_BUCKET_NAME', 'mcc-2016-g14-p2')