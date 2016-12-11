from flask import Flask
from flask_mongoengine import MongoEngine
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# Flask app
app = Flask(__name__)
app.config.from_object('config')

# Mongo instance
mongo = MongoEngine(app)

from app import views
