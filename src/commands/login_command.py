from .base_command import BaseCommannd
from src.errors.errors import Unauthorized, ApiError
import requests
import logging
import os

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

class Login(BaseCommannd):
    def __init__(self, json):
        self.email = json.get("email", "").strip()
        self.password = json.get("password", "").strip()

        API_KEY = ""
        if os.environ.get("API_KEY_FIREBASE"):
            logger.info("API KEY FIREBASE get success to production in login")
            API_KEY = os.environ.get("API_KEY_FIREBASE")

        self.FIREBASE_LOGIN_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"


    def execute(self):

        payload = {
            "email": self.email,
            "password": self.password,
            "returnSecureToken": True  
        }
        
        try:
            response = requests.post(self.FIREBASE_LOGIN_URL, json=payload)
        except Exception as e:
            logger.info("Log error: error al hacer post request a firebase login url")
            raise ApiError()

        if response.status_code == 200:
            data = response.json()
            id_token = data['idToken']
            expires_in = data['expiresIn']

            return {
                "token": id_token,
                "expiresIn": expires_in,
            }
        else:
            raise Unauthorized("Usuario no autorizado")