from flask import Flask
from flask_mongoengine import MongoEngine
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.config.from_object('config')

mongo = MongoEngine(app)

# Init test users if not present in mongo already
import logic
logic.init_test_users(app.config['TEST_USERS'])

from app import views