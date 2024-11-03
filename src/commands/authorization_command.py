from .base_command import BaseCommannd
from src.errors.errors import Unauthorized, ApiError
from src.clients.manage_client import ManageClient
import requests
import logging
from flask import request
import os
import jwt

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

class Authorization(BaseCommannd):
    def __init__(self):
        self.authorization_header = request.headers.get('Authorization')

        if self.authorization_header and self.authorization_header.split(" ")[0] == "Bearer":
             self.authorization_header = self.authorization_header.split(" ")[1]

        API_KEY = ""
        if os.environ.get("API_KEY_FIREBASE"):
            logger.info("API KEY FIREBASE get success to production in authorization")
            API_KEY = os.environ.get("API_KEY_FIREBASE")

        self.FIREBASE_AUTHORIZATION_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={API_KEY}"


    def execute(self):
        payload = {
            "idToken": self.authorization_header,
        }
        
        try:
            response = requests.post(self.FIREBASE_AUTHORIZATION_URL, json=payload)
        except Exception as e:
            logger.info("Log error: error al hacer post request a firebase authorization url")
            raise ApiError()
        
        if response.status_code == 200:
            json_data_token = jwt.decode(self.authorization_header, options={"verify_signature": False})
            user_id = json_data_token.get("user_id")
            response_data_user = self.getDataUser(user_id=user_id)
            data_user = response_data_user.json()

            return {
                "rol": data_user.get("rol"),
                "company": data_user.get("company"),
                "plan": data_user.get("plan")
            }
        else:
            error_data = response.json()
            error_message = error_data.get("error", {}).get("message", "Error desconocido")
            if error_message == "INVALID_ID_TOKEN":
                    raise Unauthorized(f"La sesión expiró")
            
    def getDataUser(self, user_id):
        try:
            return ManageClient().get_data_user(user_id)
        except Exception as e:
            logger.info("Log error: service manejo clientes con excepcion para obtener data del usuario")
            raise ApiError()