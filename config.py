import os

UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', '/images')
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

SECRET_KEY = os.environ.get('SECRET_KEY', 'development key')
SALT = os.environ.get('SALT', 'fV3Q26FcTz2DsHFf')

SESSION_TYPE = os.environ.get('SESSION_TYPE', 'filesystem')

# Mongo connection
MONGO_HOST = os.environ.get('MONGO_HOST', 'localhost')
MONGO_REPLICA_SET = os.environ.get('MONGO_REPLICA_SET', None)
MONGO_DBNAME = os.environ.get('MONGO_DBNAME', 'remote_ocr')
