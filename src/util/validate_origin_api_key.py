import os
from src.errors.errors import Forbidden
import logging

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

class ValidateOriginApiKey:
    def __init__(self, transaction_key, transaction_auth):
        self.transaction_key = transaction_key
        self.transaction_auth = transaction_auth

    def verify_api_Key_frontend(self):
        self.verify_api_Key_auth_api()
        if not self.transaction_auth and self.transaction_key != os.environ.get("API_KEY_FRONTEND"):
            logger.info("Api key recibida no corresponde a la del frontend")
            raise Forbidden("Acceso denegado al origen de la petición")
        
    def verify_api_Key_mobile(self):
        self.verify_api_Key_auth_api()
        if not self.transaction_auth and self.transaction_key != os.environ.get("API_KEY_MOBILE"):
            logger.info("Api key recibida no corresponde a la de mobile")
            raise Forbidden("Acceso denegado al origen de la petición")
        
    def verify_api_Key_auth_api(self):
        if self.transaction_auth and self.transaction_auth != os.environ.get("API_KEY_AUTH_API"):
            logger.info("Api key recibida no corresponde a la de auth-api")
            raise Forbidden("Acceso denegado")