from flask import Flask, jsonify
from src.errors.errors import ApiError

from src.blueprints.ping import ping_blueprint
from src.blueprints.authentication import authentication_blueprint

import os
import traceback
import logging

app = Flask(__name__)

app_context = app.app_context()
app_context.push()


app.register_blueprint(ping_blueprint)
app.register_blueprint(authentication_blueprint)

logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))
logger = logging.getLogger(__name__)

@app.errorhandler(ApiError)
def handle_exception(err):
    trace = traceback.format_exc()
    logger.info("Log error: " + str(trace))
    return jsonify({"message": err.description}), err.code


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)