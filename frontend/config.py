import os

# Secret authorization key
BACKEND_AUTORIZATION_KEY = os.environ.get('BACKEND_AUTORIZATION_KEY', 'secret_token')
BACKEND_IP = os.environ.get('BACKEND_IP', 'http://127.0.0.1:8080')