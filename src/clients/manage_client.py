import requests
import os
from src.errors.errors import Unavailable, Bad_Request

class ManageClient:
    def __init__(self):
        self.gateway_path = "http://gateway:5000"
        if os.environ.get("GATEWAY_PATH"):
            self.gateway_path = os.environ.get("GATEWAY_PATH")
        self.manage_client_url = f'{self.gateway_path}/clients/create_client'
        self.headers = {"Content-Type": "application/json"}

    def register_client(self, data):
        try:
            response = requests.post(self.manage_client_url, json=data, headers=self.headers)
        
            if response.status_code == 400:
                raise Bad_Request(response.json().get("msg", "Error en los campos, por favor revise la informacion ingresada"))
            return response.json()
        
        except requests.exceptions.ConnectionError:
            raise Unavailable()
    