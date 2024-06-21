from flask import request
from flask_restx import Resource

from Outback.model import UserModel
from Outback.service import save_user, get_user_by_id, get_user_by_email, set_user_individual_data

_user_api = UserModel.user_api
_user = UserModel.user
_project_log = UserModel.user_project_log
