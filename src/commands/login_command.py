from .base_command import BaseCommannd
from src.errors.errors import Unauthorized
import requests

class Login(BaseCommannd):
    def __init__(self, json):
        self.email = json.get("email", "").strip()
        self.password = json.get("password", "").strip()

    def execute(self):
        API_KEY = ""
        FIREBASE_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={API_KEY}"

        payload = {
            "email": self.email,
            "password": self.password,
            "returnSecureToken": True  
        }
        
        response = requests.post(FIREBASE_URL, json=payload)

        if response.status_code == 200:
            data = response.json()
            id_token = data['idToken']
            refresh_token = data['refreshToken']
            expires_in = data['expiresIn']
            local_id = data['localId']

            return {
                "idToken": id_token,
                "refreshToken": refresh_token,
                "expiresIn": expires_in,
                "localId": local_id
            }
        else:
            raise Unauthorized("Usuario no autorizado")
        