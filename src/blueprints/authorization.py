from flask import Blueprint

from src.commands.authorization_command import Authorization

authorization_blueprint = Blueprint('authorization', __name__)

@authorization_blueprint.route('/auth/verify-authorization', methods = ['GET'])
def verify_authorization():
    response = Authorization().execute()
    return response, 200