from flask import request
from flask_restx import Resource

from Outback.model import UserModel
from Outback.service import (
    save_user, login, verify_email, verify_email_resend, update_user, delete_user,
    get_user_by_id, get_user_by_email, decimal_to_float, token_required
)

_user_api = UserModel.user_api
_user = UserModel.user
_login = UserModel.login_model
_project_log = UserModel.user_project_log


@_user_api.route('/<int:_id>')
@_user_api.doc(id='UserID', description='User id와 관련된 API')
class UserID(Resource):
    @_user_api.doc(id='get_user_by_id', description='id로 user 정보를 불러오는 API')
    def get(self, _id):
        flag, item = get_user_by_id(_id)
        item['password'] = None
        if flag:
            decimal_to_float(item)
            return item
        else:
            return {'message': 'user not found'}, 404

    @_user_api.doc(id='update_user', description='user 정보 update')
    def post(self, _id):
        data = request.json
        exist_flag, item = get_user_by_id(_id)
        if exist_flag:
            item = decimal_to_float(item)
            flag, response = update_user(item['uuid'], item['id'], data)
            if flag:
                return {'message': 'updated successfully'}, 200
            else:
                return response, 401
        else:
            return {'message': 'user not found'}, 404

    @_user_api.doc(id='delete_user', description='user delete')
    def delete(self, _id):
        exist_flag, item = get_user_by_id(_id)
        if exist_flag:
            flag, response = delete_user(item['uuid'], item['id'])
            if flag:
                return {'message': 'delete success'}, 200
            else:
                return response, 401
        else:
            return {'message': 'user not found'}, 404


@_user_api.route('/auth')
@_user_api.doc(id='auth', description='회원 가입 관련 api')
class Auth(Resource):
    @_user_api.doc(id='user_auth', description="회원 가입")
    @_user_api.expect(_user, validate=True)
    def post(self):
        data = request.json
        check_email, item = get_user_by_email(data['email'])
        if check_email:
            return {'message': 'user exists'}, 200
        else:
            flag, item = save_user(data)
            if flag:
                return item, 200
            else:
                return {'message': item}, 401


@_user_api.route('/verify')
@_user_api.doc(id='Verify', description='이메일 인증')
class Verify(Resource):
    @_user_api.doc(id='email_verify', description='이메일 인증')
    def post(self):
        data = request.json
        email = data['email']
        cert_number = data['cert_number']

        flag, response = verify_email(email, cert_number)
        print(response)
        if flag:
            return {'message': 'email verified'}, 200
        else:
            return {'message': response}, 401


@_user_api.route('/resend')
@_user_api.doc(id='Resend', description='인증 이메일 재전송')
class Resend(Resource):
    @_user_api.doc(id='resend_email', description='인증 이메일 재전송')
    def post(self):
        data = request.json
        flag, response = verify_email_resend(data['email'])
        if flag:
            return {'message': 'email resent'}, 200
        else:
            return {'message': response}, 401


@_user_api.route('/login')
@_user_api.doc(id='login', description='로그인 관련 api')
class Login(Resource):
    @_user_api.doc(id='user_login', description='로그인')
    @_user_api.expect(_login, validate=True)
    def post(self):
        data = request.json
        email = data['email']
        password = data['password']

        try:
            flag, token, userid = login(email, password)
            if flag:
                return {'token': token, 'userid': userid, 'message': 'login success'}, 200
            else:
                return {'token': token, 'userid': userid, 'message': token}, 401
        except Exception as e:
            return {'token': None, 'userid': None, 'message': str(e)}, 401


@_user_api.route('/logout')
@_user_api.doc(id='logout', description='로그아웃 관련 api')
class Logout(Resource):
    @_user_api.doc(id='user_logout', description='로그아웃')
    def post(self):
        access_token = request.headers.get('Authorization')
        try:
            return {'message': 'logged out'}, 200
        except Exception as e:
            return {'message': str(e)}, 401
