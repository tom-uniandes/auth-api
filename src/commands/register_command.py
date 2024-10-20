from .base_command import BaseCommannd
from firebase_admin import auth as firebase_auth
from src.errors.errors import Conflict, ApiError, Bad_Request
from src.clients.manage_client import ManageClient

class Register(BaseCommannd):
    def __init__(self, json):
        self.name = json.get('name', '').strip()
        self.email = json.get('email', '').strip().lower()
        self.password = json.get("password", "").strip()
        self.id_number = json.get('idNumber', '').strip()
        self.phone_number = json.get('phoneNumber', '').strip()
        self.company = json.get('company', '')

    def execute(self):
        user = ""
        try:
            user = firebase_auth.create_user(email=self.email, password=self.password)
            data = {
                "id":user.uid,
                "name":self.name,
                "email":self.email,
                "idNumber":self.id_number,
                "phoneNumber":self.phone_number,
                "company":self.company
            }
            ManageClient().register_client(data)
            return {'message': 'Registro exitoso'}
        except firebase_auth.EmailAlreadyExistsError:
            raise Conflict(f"El usuario con el correo {self.email} ya se encuentra registrado")
        except firebase_auth.auth.AuthError as e:
            if 'WEAK_PASSWORD' in str(e):
                raise Bad_Request(f"La contraseña es muy corta")
            raise ApiError()
        except Exception as e:
            if user:
                firebase_auth.delete_user(user.uid)
            raise ApiError()

    
    