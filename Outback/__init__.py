from flask import Flask
from flask_cors import CORS
from flask_restx import Api

from Outback.api import add_namespaces
from Outback.migration import dynamodb, create_tables
from Outback.service import bcrypt


def create_app():
    app = Flask(__name__)
    app.logger.setLevel("INFO")

    # CORS(app, resources={r"/*": {"origins": "*"}})
    CORS(app)
    bcrypt.init_app(app)

    api = Api(
        app,
        version='1.0',
        title='Outback',
        description='Project Recruitment Platform',
    )

    add_namespaces(api)

    create_tables()

    return app
