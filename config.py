import os

UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', '/images')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

SECRET_KEY = os.environ.get('SECRET_KEY', 'development key')
SALT = 'fV3Q26FcTz2DsHFf'

SESSION_TYPE = os.environ.get('SESSION_TYPE', 'filesystem')

# Mongo connection
MONGODB_HOST = os.environ.get('MONGODB_HOST', 'localhost')
MONGODB_DB = os.environ.get('MONGODB_DB', 'remote_ocr')

# Test users file
TEST_USERS = os.environ.get('TEST_USERS', 'users.json')