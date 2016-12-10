from app import mongo
from mongoengine.queryset import DoesNotExist


class Users(mongo.Document):
    username = mongo.StringField(required=True)
    password = mongo.StringField(required=False)

    @staticmethod
    def get_user(username):
        try:
            return Users.objects.get(username=username)
        except DoesNotExist:
            return None


class History(mongo.Document):
    user = mongo.StringField(required=True)
    thumbnail = mongo.StringField(required=False)
    timestamp = mongo.StringField(required=True)
    text = mongo.StringField(required=True)
    source_files = mongo.ListField(required=False)

    @staticmethod
    def get_history_by_user(username):
        return History.objects(user=username)

    @staticmethod
    def get_expired(expiration):
        return History.objects(timestamp__lt=expiration)
