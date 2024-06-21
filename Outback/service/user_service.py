import uuid
import time
import random

from boto3.dynamodb.conditions import Attr

from Outback.config import Config
from Outback.migration import dynamodb

user_table = dynamodb.Table(Config.USER_TABLE_NAME)


def save_user(user):
    dtime = int(time.time() * 1000000)
    item = {
        'uuid': str(uuid.uuid4()),
        'id': (dtime * 100000000) + random.randint(0, 99999999),
        'email': user['email'],
        'password': user['password'],
        'nickname': user['nickname'],
        'note': user['note'],
        'description': user['description'],
        'range': user['range'],
        'position': user['position'],
        'stack': user['stack'],
        'projectLog': user['projectLog'],
    }

    try:
        response = user_table.put_item(Item=item)
        return True, response
    except Exception as e:
        return False, str(e)


def get_user_by_id(_id):
    try:
        response = user_table.get_item(FilterExpression=Attr('id').eq(_id))
        if response['Item'][0] is None:
            return True, None
        else:
            return True, response['Item'][0]
    except Exception as e:
        return False, str(e)


def get_user_by_email(email):
    try:
        response = user_table.get_item(FilterExpression=Attr('email').eq(email))
        if response['Item'][0] is None:
            return True, None
        else:
            return True, response['Item'][0]
    except Exception as e:
        return False, str(e)


def get_user_by_nickname(nickname):
    try:
        response = user_table.get_item(FilterExpression=Attr('nickname').eq(nickname))
        if response['Item'][0] is None:
            return True, None
        else:
            return True, response['Item'][0]
    except Exception as e:
        return False, str(e)


def get_user_list():
    try:
        response = user_table.get_items()
        if response['Item'] is None:
            return True, None
        else:
            return True, response['Item']
    except Exception as e:
        return False, str(e)


def set_user_individual_data(_id, index, data):
    try:
        response = user_table.update_item(
            key={
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


def add_project_log(_id):
    try:
        response = user_table.update_item(

        )
        return True, response['Item']
    except Exception as e:
        return False, str(e)