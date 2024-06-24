import uuid
import time
import random

from boto3.dynamodb.conditions import Attr

from .auth import hash_password
from Outback.config import Config
from Outback.migration import dynamodb, cognito

user_table = dynamodb.Table(Config.USER_TABLE_NAME)


def save_user(user):
    dtime = int(time.time() * 1000000 % 1000000000000)
    item = {
        'uuid': str(uuid.uuid4()),
        'id': (dtime * 1000000) + random.randint(0, 99999),
        'email': user['email'],
        'password': hash_password(user['password']),
        'nickname': user['nickname'],
        'note': user['note'],
        'description': user['description'],
        'range': user['range'],
        'position': user['position'],
        'stack': user['stack'],
        'projectLog': user['projectLog'],
    }

    try:
        db_response = user_table.put_item(Item=item)
        cg_response = cognito.sign_up(
            ClientId=Config.COGNITO_CLIENT_ID,
            Username=user['email'],
            Password=user['password'],
            UserAttributes=[
                {
                    'Name': "email",
                    'Value': user['email']
                },
                {
                    'Name': "nickname",
                    'Value': user['nickname']
                }
            ]
        )
        return True, cg_response
    except Exception as e:
        return False, str(e)


def verify_email(email, cert_number):
    try:
        response = cognito.confirm_sign_up(
            ClientId=Config.COGNITO_CLIENT_ID,
            Username=email,
            ConfirmationCode=cert_number
        )
        return True, response
    except Exception as e:
        return False, str(e)


def verify_email_resend(email):
    try:
        response = cognito.resend_confirmation_code(
            ClientId=Config.COGNITO_CLIENT_ID,
            Username=email
        )
        return True, response
    except Exception as e:
        return False, str(e)


def login(email, password):
    user = get_user_by_email(email)
    if not user:
        return False, {'message': 'User not found'}
    else:
        try:
            response = cognito.initiate_auth(
                ClientId=Config.COGNITO_CLIENT_ID,
                AuthFlow='USER_PASSWORD_AUTH',
                AuthParameters={
                    'USERNAME': email,
                    'PASSWORD': password
                }
            )
            token = response['AuthenticationResult']['AccessToken']

            return True, token
        except Exception as e:
            return False, {'message': str(e)}


def get_user_by_id(_id):
    try:
        response = user_table.scan(FilterExpression=Attr('id').eq(_id))
        if response['Items'][0]:
            return True, response['Items'][0]
        else:
            return False, None
    except Exception as e:
        return False, str(e)


def get_user_by_email(email):
    try:
        response = user_table.scan(FilterExpression=Attr('email').eq(email))
        if response['Items'][0]:
            return True, response['Items'][0]
        else:
            return False, None
    except Exception as e:
        return False, str(e)


def update_user(_uuid, _id, data):
    try:
        response = user_table.update_item(
            Key={
                'uuid': _uuid,
                'id': _id
            },
            UpdateExpression='SET #t1=:val1, #t2=:val2, #t3=:val3, #t4=:val4, #t5=:val5, #t6=:val6',
            ExpressionAttributeNames={
                '#t1': 'nickname',
                '#t2': 'note',
                '#t3': 'description',
                '#t4': 'range',
                '#t5': 'position',
                '#t6': 'stack'
            },
            ExpressionAttributeValues={
                ':val1': data['nickname'],
                ':val2': data['note'],
                ':val3': data['description'],
                ':val4': data['range'],
                ':val5': data['position'],
                ':val6': data['stack']
            }
        )
        return True, response
    except Exception as e:
        return False, str(e)


def set_user_individual_data(_id, index, data):
    try:
        response = user_table.update_item(
            Key={
                'id': _id
            },
            updateExpression='SET #index = :val1',
            ExpressionAttributeNames={
                '#index': index
            },
            ExpressionAttributeValues={
                ':val1': data
            }
        )
        return True, response
    except Exception as e:
        return False, str(e)


def add_project_log(_uuid, _id):
    try:
        response = user_table.update_item(

        )
        return True, response['Item']
    except Exception as e:
        return False, str(e)


def delete_user(_uuid, _id):
    try:
        response = user_table.delete_item(
            Key={
                'uuid': _uuid,
                'id': _id
            }
        )
        return True, response
    except Exception as e:
        return False, str(e)
