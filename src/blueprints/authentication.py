from flask import jsonify, request, Blueprint

from src.commands.register_command import Register
from src.commands.ping_command import Ping

authentication_blueprint = Blueprint('authentication', __name__)

@authentication_blueprint.route('/register', methods = ['POST'])
def register():
    json = request.get_json()
    response = Register(json).execute()
    return jsonify(response), 201

@authentication_blueprint.route('/login', methods = ['POST'])
def login():
    response = Ping().execute()
    return response, 200