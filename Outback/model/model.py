from flask_restx import Namespace, fields


class UserModel:
    user_api = Namespace('User', description='User operations', path='/user')
    user_project_log = user_api.model(
        'UserProjectLog',
        {
            'uuid': fields.String(required=True, description='UUID of the joined project'),
            'id': fields.Integer(required=True, description='ID of the joined project'),
            'name': fields.String(required=True, description='Name of the joined project'),
            'description': fields.String(required=True, description='Description of the joined project'),
            'position': fields.String(required=True, description='Position of the joined project'),
        }
    )
    user = user_api.model(
        'User',
        {
            'id': fields.Integer(required=True, description='User id'),
            'email': fields.String(required=True, description='User email'),
            'password': fields.String(required=True, description='User password'),
            'nickname': fields.String(required=True, description='User nickname'),
            'note': fields.String(description='User note'),
            'description': fields.String(description='User description'),
            'range': fields.List(fields.String, required=True, description='User range'),
            'position': fields.List(fields.String, required=True, description='User position'),
            'stack': fields.List(fields.String, required=True, description='User stack'),
            'projectLog': fields.List(
                fields.Nested(
                    description='User project log',
                    model=user_project_log
                ),
                description='User project log'
            ),
        }
    )


class ProjectModel:
    project_api = Namespace('Project', description='Project operations', path='/project')

    project_wanted = project_api.model(
        'ProjectWanted',
        {
            'stack': fields.String(required=True, description='Project stack'),
            'personal': fields.Integer(required=True, description='Project personal'),
        }
    )

    comment = project_api.model(
        'Comment',
        {
            'uuid': fields.String(required=True, description='UUID of the comment'),
            'id': fields.Integer(required=True, description='ID of the comment'),
            'content': fields.String(required=True, description='Content of the comment'),
            'projectId': fields.Integer(required=True, description='Project id'),
            'parentId': fields.Integer(required=True, description='ID of the parent project'),
            'userId': fields.Integer(required=True, description='User id'),
            'datetime': fields.String(required=True, description='datetime of the comment'),
        }
    )

    project = project_api.model(
        'Project',
        {
            'id': fields.Integer(required=True, description='Project id'),
            'name': fields.String(required=True, description='Project name'),
            'description': fields.String(required=True, description='Project description'),
            'category': fields.String(required=True, description='Project 분야'),
            'stack': fields.List(fields.String, required=True, description='Project stack'),
            'wanted': fields.List(project_wanted, required=True, description='Project 구인'),
            'inNow': fields.List(project_wanted, required=True, description='Project 현재 인원'),
            'status': fields.String(required=True, description='Project status'),
            'publisher': fields.String(required=True, description='Project publisher'),
            'endDate': fields.String(required=True, description='Project end date'),
            'modifiedDate': fields.String(required=True, description='Project modified date'),
            'comment': fields.Nested(
                description='Project comment',
                model=comment
            )
        }
    )