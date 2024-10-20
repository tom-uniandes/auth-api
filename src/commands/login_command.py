from .base_command import BaseCommannd

class Login(BaseCommannd):
    def __init__(self, json):
        self.email = json.get("email", "").strip()
        self.password = json.get("password", "").strip()

    def execute(self):
        return "pong"