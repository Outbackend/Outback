from .project import _project_api
from .user import _user_api


def add_namespaces(api):

    api.add_namespace(_project_api)
    api.add_namespace(_user_api)
