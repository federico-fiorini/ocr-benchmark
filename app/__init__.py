from flask import Flask
from flask_mongoengine import MongoEngine
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.config.from_object('config')

mongo = MongoEngine(app)

from app import views