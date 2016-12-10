from flask import Flask
from celery import Celery
from celery.schedules import crontab
from flask_mongoengine import MongoEngine
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

# Flask app
app = Flask(__name__)
app.config.from_object('config')

# Mongo instance
mongo = MongoEngine(app)

# Init test users if not present in mongo already
import logic
logic.init_test_users(app.config['TEST_USERS'])

from app import views


# Celery instance
celery_app = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery_app.conf.update(app.config)

import tasks


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):

    # Executes every day at midnight
    sender.add_periodic_task(
        # crontab(minute=0, hour=0),
        crontab(minute='*/1'),
        tasks.delete_expired_images.s(),
    )