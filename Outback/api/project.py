from flask import request
from flask_restx import Resource

from Outback.model import ProjectModel
from Outback.service import save_project, add_comment, get_project_list, get_project_by_id, update_project

_project_api = ProjectModel.project_api
_project = ProjectModel.project
_project_wanted = ProjectModel.project_wanted
_comment = ProjectModel.comment


@_project_api.route('/list')
@_project_api.doc(id='project_list', description='Project 관련')
class Project(Resource):
    @_project_api.doc(id='get_project_list', description='Project list를 return하는 api')
    def get(self):
        flag, items = get_project_list()
        if flag:
            return items, 200
        else:
            return items, 401


@_project_api.route('/add')
class AddProject(Resource):
    @_project_api.doc(id='add_project', description='Project를 추가하는 api')
    @_project_api.expect(_project, validate=True)
    def post(self):
        data = request.json()
        flag, response = save_project(data)
        if flag:
            return response, 200
        else:
            return response, 401


@_project_api.route('/<int:_id>')
class ProjectById(Resource):
    @_project_api.doc(id='get_project_by_id', description='id로 Project 불러오기')
    def get(self, _id):
        flag, response = get_project_by_id(_id)
        if flag:
            return response, 200
        else:
            return response, 401

    @_project_api.doc(id='update_project', description='project update')
    @_project_api.expect(_project, validate=True)
    def post(self, _id):
        data = request.json()
        flag, response = update_project(data)
        if flag:
            return response, 200
        else:
            return response, 401


@_project_api.route('/<int:_id>/comment')
@_project_api.expect(_comment, validate=True)
@_project_api.doc(id='add_comment', description='댓글 추가')
class Comment(Resource):
    def post(self, _id):
        data = request.json()
        flag, response = add_comment(_id, data['userId'], data['parentId'], data['content'])
        if flag:
            return response, 200
        else:
            return response, 401
