from .base_command import BaseCommannd
from src.errors.errors import Unauthorized, ApiError
from src.clients.manage_client import ManageClient
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
            user_id = data['localId']
            expires_in = data['expiresIn']

            response_data_user = self.getDataUser(user_id=user_id)
            data_user = response_data_user.json()

            return {
                "token": id_token,
                "expiresIn": expires_in,
                "rol": data_user.get("rol"),
                "company": data_user.get("company"),
                "plan": data_user.get("plan")
            }
        else:
            raise Unauthorized("Correo y/o contraseña incorrecta")
        
    def getDataUser(self, user_id):
        try:
            return ManageClient().get_data_user(user_id)
        except Exception as e:
            logger.info("Log error: service manejo clientes con excepcion para obtener data del usuario")
            raise ApiError()