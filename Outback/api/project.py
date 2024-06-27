from flask import request
from flask_restx import Resource
from flask_cognito import cognito_auth_required, current_cognito_jwt

from Outback.model import ProjectModel
from Outback.service import (
    get_project_list, get_project_by_id, get_comment, get_comment_list,
    save_project, add_comment, update_project, update_comment, delete_project, delete_comment,
    decimal_to_float, get_user_by_header
)

_project_api = ProjectModel.project_api
_project = ProjectModel.project
_project_wanted = ProjectModel.project_wanted
_project_comment = ProjectModel.project_comment
_comment = ProjectModel.comment


@_project_api.route('/list')
@_project_api.doc(id='project_list', description='Project 관련')
class ProjectList(Resource):
    @_project_api.doc(id='get_project_list', description='Project list를 return하는 api')
    def get(self):
        flag, items = get_project_list()
        if flag:
            for i in range(0, len(items)):
                items[i] = decimal_to_float(items[i])
            return items, 200
        else:
            return items, 401


@_project_api.route('/add')
class AddProject(Resource):
    @_project_api.doc(id='add_project', description='Project를 추가하는 api')
    @_project_api.expect(_project, validate=True)
    @cognito_auth_required
    def post(self):
        data = request.json
        save_flag, project_id = save_project(data)
        if save_flag:
            get_flag, items = get_project_by_id(project_id)
            if get_flag:
                return decimal_to_float(items), 200
            else:
                return items, 200
        else:
            return project_id, 401


@_project_api.route('/<int:_id>')
@_project_api.doc(id='project')
class Project(Resource):
    @_project_api.doc(id='get_project_by_id', description='id로 Project 불러오기')
    def get(self, _id):
        flag, response = get_project_by_id(_id)
        if flag:
            return decimal_to_float(response), 200
        else:
            return response, 401

    @_project_api.doc(id='update_project', description='project update')
    @_project_api.expect(_project, validate=True)
    @cognito_auth_required
    def post(self, _id):
        header = request.headers.get('Authorization')
        cg_flag, cg_user = get_user_by_header(header)
        data = request.json
        exist_flag, item = get_project_by_id(_id)
        if exist_flag and cg_flag:
            if item['publisher'] != cg_user['id']:
                return {'message': 'user not matched'}, 401
            flag, response = update_project(item['uuid'], item['id'], data)
            if flag:
                return decimal_to_float(response), 200
            else:
                return response, 401
        else:
            return {'message': 'error'}, 401

    @_project_api.doc(id='delete_project', description='project delete')
    @cognito_auth_required
    def delete(self, _id):
        header = request.headers.get('Authorization')
        cg_flag, cg_user = get_user_by_header(header)
        exist_flag, item = get_project_by_id(_id)
        if exist_flag and cg_flag:
            if item['publisher'] != cg_user['id']:
                return {'message': 'user not matched'}, 401
            flag, response = delete_project(item['uuid'], item['id'])
            if flag:
                return {'message': 'delete success'}, 200
            else:
                return response, 401
        else:
            return {'message': 'not found'}, 401


@_project_api.route('/<int:_id>/comment')
@_project_api.doc(id='add_comment', description='댓글 관련 api')
class Comment(Resource):
    @_project_api.doc(id='get_comment_list', description='댓글 리스트')
    def get(self, _id):
        flag, items = get_comment_list(_id)
        if flag:
            for i in range(0, len(items)):
                items[i] = decimal_to_float(items[i])
            return items, 200
        else:
            return items, 401

    @_project_api.doc(id='add_comment', description='댓글 추가')
    @_project_api.expect(_comment, validate=True)
    @cognito_auth_required
    def post(self, _id):
        header = request.headers.get('Authorization')
        cg_flag, cg_user = get_user_by_header(header)
        data = request.json
        exist_flag, item = get_project_by_id(_id)
        print(cg_user['id'])
        if exist_flag:
            if data['userId'] != cg_user['id']:
                return {'message': "user not matched."}, 404
            flag, response = add_comment(item['uuid'], item['id'], data['userId'], data['parentId'], data['content'])
            if flag:
                return {'message': 'success'}, 200
            else:
                return response, 401

    @_project_api.doc(id='update_comment', description='댓글 수정')
    @_project_api.expect(_comment, validate=True)
    @cognito_auth_required
    def patch(self, _id):
        header = request.headers.get('Authorization')
        cg_flag, cg_user = get_user_by_header(header)
        data = request.json
        exist_flag, item = get_comment(data['id'])
        if exist_flag:
            if data['userId'] != cg_user['id']:
                return {'message': "user not matched."}, 404
            flag, response = update_comment(item['uuid'], item['id'], data['content'])
            if flag:
                return {'message': 'success'}, 200
            else:
                return response, 401
        else:
            return {'message': 'comment not found'}, 401

    @_project_api.doc(id='delete_comment', description='댓글 삭제')
    @cognito_auth_required
    def delete(self, _id):
        header = request.headers.get('Authorization')
        cg_flag, cg_user = get_user_by_header(header)
        data = request.json
        exist_flag, item = get_comment(data['commentId'])
        if exist_flag:
            if item['userId'] != cg_user['id']:
                return {'message': "user not matched."}, 404
            flag, response = delete_comment(item['uuid'], item['id'])
            if flag:
                return {'message': 'success'}, 200
            else:
                return response, 401
        else:
            return {'message': 'comment not found'}, 401
