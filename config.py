import os

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

SECRET_KEY = os.environ.get('SECRET_KEY', 'development key')
SALT = os.environ.get('SALT', 'fV3Q26FcTz2DsHFf')

SESSION_TYPE = os.environ.get('SESSION_TYPE', 'filesystem')
