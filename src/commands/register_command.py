from .base_command import BaseCommannd
from src.errors.errors import Conflict, ApiError, Bad_Request, Unavailable
from src.clients.manage_client import ManageClient
import requests
import logging
import os

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

class Register(BaseCommannd):
    def __init__(self, json):
        self.name = json.get('name', '').strip()
        self.email = json.get('email', '').strip().lower()
        self.password = json.get("password", "").strip()
        self.id_type = json.get('idType', '').strip()
        self.id_number = json.get('idNumber', '').strip()
        self.phone_number = json.get('phoneNumber', '').strip()
        self.company = json.get('company', '')
        self.rol = json.get('rol', '')

        API_KEY = ""
        if os.environ.get("API_KEY_FIREBASE"):
            logger.info("API KEY FIREBASE get success to production in register")
            API_KEY = os.environ.get("API_KEY_FIREBASE")

        self.FIREBASE_SIGNUP_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signUp?key={API_KEY}"
        self.FIREBASE_DELETE_USER_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:delete?key={API_KEY}"


    def execute(self):
        self.id_token = ""
        payload = {
            "email": self.email,
            "password": self.password,
            "returnSecureToken": True 
        }

        try:
            response = requests.post(self.FIREBASE_SIGNUP_URL, json=payload)
        except Exception as e:
            logger.info("Log error: error al hacer post request a firebase signup url")
            raise ApiError()

        if response.status_code == 200:
            data = response.json()
            self.id_token = data['idToken'],
            uid = data['localId']

            data = {
                "id":uid,
                "name":self.name,
                "email":self.email,
                "idNumber":self.id_number,
                "idType":self.id_type,
                "phoneNumber":self.phone_number,
                "company":self.company,
                "rol":self.rol
            }
            self.register_client(data)
            return {'message': 'Registro exitoso'}
        else:
            error_data = response.json()
            error_message = error_data.get("error", {}).get("message", "Error desconocido")
        
            if error_message == "EMAIL_EXISTS":
                raise Conflict(f"El usuario con el correo {self.email} ya se encuentra registrado")
            elif error_message == "INVALID_EMAIL":
                raise Conflict(f"El correo {self.email} es invalido")
            elif error_message == "WEAK_PASSWORD : Password should be at least 6 characters":
                raise Bad_Request(f"La contraseña es muy corta, debe tener al menos 6 caracteres")
            else:
                self.delete_user()
                raise ApiError()

        
    def delete_user(self):
        if self.id_token:
            payload = {
                "idToken": self.id_token[0]
            }
            response = requests.post(self.FIREBASE_DELETE_USER_URL, json=payload)
            return response

    def register_client(self, data):
        try:
            response = ManageClient().register_client(data)
        except Exception as e:
            logger.info("Log error: service manejo clientes con excepcion")
            self.delete_user()
            raise ApiError()
        
        if response.status_code == 400:
            logger.info("Log error: service manejo clientes con status " + str(response.status_code))
            logger.info("Response error: " + str(response.json().get("msg")))
            self.delete_user()
            raise Bad_Request(response.json().get("msg"))
        
        if response.status_code != 201:
            logger.info("Log error: service manejo clientes con status " + str(response.status_code))
            self.delete_user()
            raise Unavailable()
            


    
    