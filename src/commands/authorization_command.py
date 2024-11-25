from ast import For
from math import log

from .base_command import BaseCommannd
from src.errors.errors import Forbidden, Unauthorized, ApiError
from src.clients.manage_client import ManageClient
from src.util.validate_origin_api_key import ValidateOriginApiKey
import requests
import logging
from flask import request, make_response, jsonify
import os
import jwt
import json

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

class Authorization(BaseCommannd):
    def __init__(self):
        self.authorization_header = request.headers.get('Authorization')
        self.transaction_key = request.headers.get('X-Abcall-Transaction')
        self.transaction_auth_key = request.headers.get('X-Abcall-Transaction-Auth')
        self.origin_request = request.headers.get('X-Abcall-Origin-Request')

        if self.authorization_header and self.authorization_header.split(" ")[0] == "Bearer":
             self.authorization_header = self.authorization_header.split(" ")[1]


    def execute(self):
        if self.transaction_auth_key and self.transaction_auth_key != os.environ.get("API_KEY_AUTH_API"):
            logger.info("Api key recibida no corresponde a la de auth-api")
            raise Forbidden("Acceso denegado al origen de la petición")
        
        if self.authorization_header and self.transaction_key and self.origin_request == "web":
            ValidateOriginApiKey(self.transaction_key, self.transaction_auth_key).verify_api_Key_frontend()
            return self.validate_access_web_authentication()
        elif self.transaction_key and self.origin_request == "web":
            ValidateOriginApiKey(self.transaction_key, self.transaction_auth_key).verify_api_Key_frontend()
            return self.validate_access_web_public()
        elif self.transaction_key and self.origin_request == "mobile":
            ValidateOriginApiKey(self.transaction_key, self.transaction_auth_key).verify_api_Key_mobile()
            return self.validate_access_mobile()
        else:
            raise Forbidden("Acceso denegado al recurso")     

    def getDataUser(self, user_id):
        try:
            return ManageClient().get_data_user(user_id)
        except Exception as e:
            logger.info("Log error: service manejo clientes con excepcion para obtener data del usuario")
            raise ApiError()
        
    def validate_access_web_authentication(self):
        payload = {
            "idToken": self.authorization_header,
        }
        
        try:
            API_KEY = ""
            if os.environ.get("API_KEY_FIREBASE"):
                logger.info("API KEY FIREBASE get success to production in authorization")
                API_KEY = os.environ.get("API_KEY_FIREBASE")

            FIREBASE_AUTHORIZATION_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={API_KEY}"
            response = requests.post(FIREBASE_AUTHORIZATION_URL, json=payload)
        except Exception as e:
            logger.info("Log error: error al hacer post request a firebase authorization url")
            raise ApiError()
        
        if response.status_code == 200:
            json_data_token = jwt.decode(self.authorization_header, options={"verify_signature": False})
            user_id = json_data_token.get("user_id")
            response_data_user = self.getDataUser(user_id=user_id)
            data_user = response_data_user.json()

            rol = data_user.get("rol")
            company = data_user.get("company")
            plan = data_user.get("plan")

            data = {
                "rol": rol,
                "company": company,
                "plan": plan
            }
            response = make_response(jsonify(data))
            name_api_key = self.verify_configuration_access_web_authentication(rol, plan)
            response.headers["X-Abcall-Transaction"] = os.environ.get(name_api_key)
            logger.info(response)
            return response
        else:
            error_data = response.json()
            error_message = error_data.get("error", {}).get("message", "Error desconocido")
            if error_message == "INVALID_ID_TOKEN":
                    raise Unauthorized(f"La sesión expiró")
    
    def validate_access_web_public(self):
        response = make_response({})
        name_api_key = self.verify_configuration_access_web_public()
        response.headers["X-Abcall-Transaction"] = os.environ.get(name_api_key)
        return response

    def validate_access_mobile(self):
        response = make_response({})
        name_api_key = self.verify_configuration_access_mobile()
        response.headers["X-Abcall-Transaction"] = os.environ.get(name_api_key)
        return response
    
    def verify_configuration_access_web_public(self):
        params = request.args
        uri_value = params.get('uri')

        configurations_access = self.loadConfigurations()
        name_api_key = ""
        data = self.searchRouteJson(configurations_access, uri_value)
        if data:
            name_api_key = data.get("name_api_key")
            origin_request = data.get("origin_request")

            if data.get("roles", {}):
                raise Forbidden("El recurso solicitado no es público")

            if self.origin_request not in origin_request:
                logger.info("El origen recibido no corresponde al esperado")
                raise Forbidden("Acceso denegado al origen de la petición")
    
        return name_api_key

    def verify_configuration_access_web_authentication(self, rol, plan):
        params = request.args
        uri_value = params.get('uri')
        configurations_access = self.loadConfigurations()
        name_api_key = ""
        data = self.searchRouteJson(configurations_access, uri_value)
        if data:
            roles = data.get("roles", {})
            name_api_key = data.get("name_api_key")
            origin_request = data.get("origin_request")

            if self.origin_request not in origin_request:
                logger.info("El origen recibido con autenticación no corresponde al esperado")
                raise Forbidden("Acceso denegado al origen de la petición")
            
            if rol in roles:
                planes_permitidos = roles[rol]
                self.searchReourceAllow(plan, planes_permitidos)
            elif not roles:
                logger.info("uri is public: " + uri_value)
            else:
                raise Forbidden(f"El rol {rol} no tiene acceso a este recurso")
    
        return name_api_key
    
    def searchReourceAllow(self, plan, planes_permitidos):
        if plan not in planes_permitidos:
            raise Forbidden(f"El plan {plan} no tiene acceso a este recurso")
    
    def verify_configuration_access_mobile(self):
        params = request.args
        uri_value = params.get('uri')

        configurations_access = self.loadConfigurations()
        name_api_key = ""
        data = self.searchRouteJson(configurations_access, uri_value)
        if data:
            name_api_key = data.get("name_api_key")
            origin_request = data.get("origin_request")

            if self.origin_request not in origin_request:
                logger.info("El origen recibido no corresponde al esperado para mobile")
                raise Forbidden("Acceso denegado al origen de la petición")
    
        return name_api_key


    def loadConfigurations(self):
        with open('configuration-access.json', 'r', encoding='utf-8') as file:
            return json.load(file)
        
    def searchRouteJson(self, configurations_access, uri_value):
        for prefix, value in configurations_access.items():
            if uri_value.startswith(prefix):
                return value 
        return None
