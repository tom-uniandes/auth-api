from .base_command import BaseCommannd
from firebase_admin import auth as firebase_auth
from src.errors.errors import Conflict, ApiError
from src.clients.manage_client import ManageClient

class Register(BaseCommannd):
    def __init__(self, json):
        self.email = json.get("email", "").strip()
        self.password = json.get("password", "").strip()

    def execute(self):
        user = ""
        try:
            user = firebase_auth.create_user(email=self.email, password=self.password)
            ManageClient().register_client(user.uid)
            return {'message': 'Registro exitoso'}
        except firebase_auth.EmailAlreadyExistsError:
            raise Conflict(f"El usuario con el correo {self.email} ya se encuentra registrado")
        except Exception as e:
            if user:
                firebase_auth.delete_user(user.uid)
            raise ApiError()

    
    