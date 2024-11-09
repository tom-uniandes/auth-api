import requests
import os
from src.errors.errors import Unavailable, Bad_Request

class ManageClient:
    def __init__(self):
        self.gateway_path = "http://gateway:5000"
        if os.environ.get("GATEWAY_PATH"):
            self.gateway_path = os.environ.get("GATEWAY_PATH")
        self.headers = {"Content-Type": "application/json"}

    def register_client(self, data):
        create_client_url = f'{self.gateway_path}/clients/create_client'
        return requests.post(create_client_url, json=data, headers=self.headers)

    def get_data_user(self, id_user):
        get_data_client_url = f'{self.gateway_path}/clients/get_client/{id_user}'
        return requests.get(get_data_client_url)
    