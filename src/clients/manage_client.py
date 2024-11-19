import requests
import os
from src.errors.errors import Unavailable, Bad_Request

class ManageClient:
    def __init__(self):
        self.gateway_path = "http://gateway:5000"
        if os.environ.get("GATEWAY_PATH"):
            self.gateway_path = os.environ.get("GATEWAY_PATH")
        self.headers = {"X-Abcall-Transaction":os.environ.get("API_KEY_AUTH_API"),
                        "X-Abcall-Origin-Request":"web"}

    def register_client(self, data):
        headers = self.headers
        headers["Content-Type"] = "application/json"
        create_client_url = f'{self.gateway_path}/clients/create_client'
        return requests.post(create_client_url, json=data, headers=headers)

    def get_data_user(self, id_user):
        get_data_client_url = f'{self.gateway_path}/clients/get_client/{id_user}'
        return requests.get(get_data_client_url, headers=self.headers)
    