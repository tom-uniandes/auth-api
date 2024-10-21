from flask import Blueprint

from src.commands.ping_command import Ping

ping_blueprint = Blueprint('ping', __name__)

@ping_blueprint.route('/ping', methods = ['GET'])
def healtcheck():
    response = Ping().execute()
    return response, 200