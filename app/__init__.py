from flask import Flask
from flask_pymongo import PyMongo
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

app = Flask(__name__)
app.config.from_object('config')

mongo = PyMongo(app, config_prefix='MONGO')

from app import views