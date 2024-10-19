from .base_command import BaseCommannd
from firebase_admin import auth as firebase_auth

class Register(BaseCommannd):
    def __init__(self, json):
        self.email = json.get("email", "").strip()
        self.password = json.get("password", "").strip()

    def execute(self):
        user = firebase_auth.create_user(email=self.email, password=self.password)
        return {'message': 'User registered successfully', 'user_id': user.uid}
    
    