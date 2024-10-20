from flask import Flask, jsonify
from src.errors.errors import ApiError

from src.blueprints.ping import ping_blueprint
from src.blueprints.authentication import authentication_blueprint

import os
import traceback
import logging
import json

import firebase_admin
from firebase_admin import credentials

app = Flask(__name__)

app_context = app.app_context()
app_context.push()


app.register_blueprint(ping_blueprint)
app.register_blueprint(authentication_blueprint)

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

def init_firebase():
    firebase_key_string = os.environ.get("PRIVATE_KEY_FIREBASE")
    json_key_fireabse = json.loads(firebase_key_string)

    with open('./abc-call-firebase-adminsdk.json', 'w') as json_file:
        json.dump(json_key_fireabse, json_file, indent=4)

    cred = credentials.Certificate("./abc-call-firebase-adminsdk.json")
    firebase_admin.initialize_app(cred)

@app.errorhandler(ApiError)
def handle_exception(err):
    trace = traceback.format_exc()
    logger.info("Log error: " + str(trace))
    return jsonify({"msg": err.description}), err.code

init_firebase()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)