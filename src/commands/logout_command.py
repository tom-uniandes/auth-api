from .base_command import BaseCommannd
import requests
import logging
from flask import request
import os
import jwt

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

class Logout(BaseCommannd):
    def __init__(self):
        self.authorization_header = request.headers.get('Authorization')

        if self.authorization_header and self.authorization_header.split(" ")[0] == "Bearer":
             self.authorization_header = self.authorization_header.split(" ")[1]

    def execute(self):
        payload = {
            "idToken": self.authorization_header,
        }
        return {"message": "Sesión cerrada exitosamente"}