from flask import Flask
from flask_cors import CORS
from flask_restx import Api

from Outback.api import add_namespace
from Outback.migration import migrate



def create_app():
    app = Flask(__name__)
    app.logger.setLevel("INFO")

    CORS(app, resources={r"/*": {"origins": "*"}})

    api = Api(
        app,
        version='1.0',
        title='Outback',
        description='Project Recruitment Platform',
    )

    add_namespaces(api)

    migrate.create_tables()

    return app
