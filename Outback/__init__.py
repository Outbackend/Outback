from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from flask_cognito import CognitoAuth

from Outback.config import Config
from Outback.api import add_namespaces
from Outback.migration import dynamodb, create_tables
from Outback.service import bcrypt


def create_app():
    app = Flask(__name__)
    app.logger.setLevel("INFO")

    CORS(app, resources={r"/*": {"origins": "*"}})

    app.config.update({
        'COGNITO_REGION': Config.AWS_REGION,
        'COGNITO_USERPOOL_ID': Config.COGNITO_USER_POOL_ID,

        # optional
        'COGNITO_APP_CLIENT_ID': Config.COGNITO_CLIENT_ID,  # client ID you wish to verify user is authenticated against
        'COGNITO_CHECK_TOKEN_EXPIRATION': False,  # disable token expiration checking for testing purposes
        'COGNITO_JWT_HEADER_NAME': 'Authorization',
        'COGNITO_JWT_HEADER_PREFIX': 'Bearer',
    })

    cognito = CognitoAuth(app)

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
