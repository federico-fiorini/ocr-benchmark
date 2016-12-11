from google.cloud import storage
from app import app
from utils import get_filename, get_filepath


class GoogleCloudStorage:

    def __init__(self):
        # Init bucket
        bucket_name = app.config['GOOGLE_BUCKET_NAME']

        storage_client = storage.Client()
        self.bucket = storage_client.get_bucket(bucket_name)

    def upload_to_cloud_storage(self, filepath):
        """
        Upload file to cloud storage
        :param filepath:
        :return:
        """
        blob = self.bucket.blob(get_filename(filepath))
        blob.upload_from_filename(filepath)

    def download_from_cloud_storage(self, filename):
        """
        Download file from cloude storage
        :param filepath:
        :return:
        """
        filepath = get_filepath(filename)
        blob = self.bucket.blob(filename)
        blob.download_to_filename(filepath)

        return filepath

    def delete_from_cloud_storage(self, filename):
        """
        Delete file from cloud storage
        :param filename:
        :return:
        """
        blob = self.bucket.blob(filename)
        blob.delete()
