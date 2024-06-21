import os


class Config:
    # DB Table
    PROJECT_TABLE_NAME = os.environ.get('PROJECT_TABLE')
    USER_TABLE_NAME = os.environ.get('USER_TABLE')
    COMMENT_TABLE = os.environ.get('COMMENT_TABLE')
