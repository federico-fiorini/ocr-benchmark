import requests
from app import app
import json


class BackEndService:

    TOKEN_SCHEME = "Bearer"
    LOGIN_ENDPOINT = '/login'

    def __init__(self):
        self.address = app.config['BACKEND_IP']
        self.headers = {
            'Authorization': '%s %s' % (self.TOKEN_SCHEME, app.config['BACKEND_AUTORIZATION_KEY']),
            'Content-Type': 'application/json'
        }

    def post_request(self, endpoint, data):
        """
        Perform POST request
        :param endpoint:
        :param data:
        :return:
        """
        return requests.post(self.prepend_host(endpoint), json.dumps(data), headers=self.headers)

    def prepend_host(self, endpoint):
        """
        Prepend host to endpoint
        :param endpoint:
        :return:
        """
        return self.address.rstrip('/') + endpoint

    def login(self, username, password):
        """
        Calls LOGIN endpoint to authenticate the user
        :param username:
        :param password:
        :return:
        """
        body = {
            "username": username,
            "password": password
        }
        response = self.post_request(self.LOGIN_ENDPOINT, body)
        if response.status_code == 200:
            return True
        else:
            return False
