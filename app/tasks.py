from app import app, celery_app
from models import History
from datetime import datetime, timedelta
import isodate
from utils import delete_file


@celery_app.task
def delete_expired_images():

    # Get expiration day
    days = int(app.config['SOURCE_IMAGE_LIFETIME'])
    expiration = isodate.datetime_isoformat(datetime.now() - timedelta(days=days))

    # Get expired history
    history_list = History.get_expired(expiration)

    files_to_delete = []
    for history in history_list:

        # Get images to delete
        files = history.source_files
        files_to_delete += files

        # Update mongo
        history.source_files = []
        history.save()

    # Delete all files to delete
    for image in files_to_delete:
        delete_file(image)