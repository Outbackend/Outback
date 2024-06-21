import os


class Config:
    # DB Table
    PROJECT_TABLE_NAME = os.environ.get('PROJECT_TABLE')
    USER_TABLE_NAME = os.environ.get('USER_TABLE')
    COMMENT_TABLE = os.environ.get('COMMENT_TABLE')

    t1 = os.environ.get('AWS_REGION')
    t2 = os.environ.get('AWS_ACCESS_KEY_ID')
    t3 = os.environ.get('AWS_SECRET_ACCESS_KEY')
