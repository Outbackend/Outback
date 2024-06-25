import os


class Config:
    # DB Table
    PROJECT_TABLE_NAME = os.environ.get('PROJECT_TABLE')
    USER_TABLE_NAME = os.environ.get('USER_TABLE')
    COMMENT_TABLE = os.environ.get('COMMENT_TABLE')

    # Bcrypt Secret Key
    BCRYPT_SECRET_KEY = os.environ.get('BCRYPT_SECRET_KEY')

    # JWT Secret Key
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

    # Cognito
    COGNITO_USER_POOL_ID = os.environ.get('COGNITO_USER_POOL_ID')
    COGNITO_CLIENT_ID = os.environ.get('COGNITO_CLIENT_ID')
    COGNITO_CLIENT_SECRET = os.environ.get('COGNITO_CLIENT_SECRET')

    # AWS Region
    AWS_REGION = os.environ.get('AWS_REGION')
