import uuid
import time
import random

from datetime import datetime
from pytz import timezone
from boto3.dynamodb.conditions import Attr

from Outback.config import Config
from Outback.migration import dynamodb

project_table = dynamodb.Table(Config.PROJECT_TABLE_NAME)
comment_table = dynamodb.Table(Config.COMMENT_TABLE)


def save_project(project):
    now = datetime.now(timezone('Asia/Seoul'))
    dtime = int(time.time() * 1000000)
    item = {
        'uuid': str(uuid.uuid4()),
        'id': (dtime * 100000000) + random.randint(10000001, 30000000),
        'name': project['name'],
        'description': project['description'],
        'category': project['category'],
        'stack': project['stack'],
        'wanted': project['wanted'],
        'inNow': project['inNow'],
        'status': project['status'],
        'publisher': project['publisher'],
        'endDate': project['endDate'],
        'modifiedDate': now.strftime('%Y-%m-%d %H:%M:%S'),
        'comment': None,
    }
    try:
        response = project_table.put_item(Item=item)
        return True, response
    except Exception as e:
        return False, str(e)


def add_comment(project_id, user_id, parent_id, content):
    now = datetime.now(timezone('Asia/Seoul'))
    dtime = int(time.time() * 1000000)
    item = {
        'uuid': str(uuid.uuid4()),
        'id': (dtime * 100000000) + random.randint(30000001, 99999999),
        'content': content,
        'projectId': project_id,
        'parentId': parent_id,
        'userId': user_id,
        'datetime': now.strftime('%Y-%m-%d %H:%M:%S')
    }
    try:
        update_response = project_table.update_item(
            Key={
                'id': item['id']
            },
            UpdateExpression='SET #comment = list_append(#comment, :comment)',
            ExpressionAttributeNames={
                '#comment': 'comment'
            },
            ExpressionAttributeValues={
                ':comment': item
            },
            ReturnValues='UPDATED_NEW'
        )
        add_response = comment_table.put_item(Item=item)
        response = {'update_response': update_response, 'add_response': add_response}
        return True, response
    except Exception as e:
        return False, str(e)


def get_comment_list(project_id):
    try:
        response = comment_table.scan(
            FilterExpression=Attr('projectId').eq(project_id)
        )
        return True, response['Items']
    except Exception as e:
        return False, str(e)


def set_user_individual_data(_id, index, data):
    now = datetime.now(timezone('Asia/Seoul'))
    try:
        response = project_table.update_item(
            key={
                'id': _id
            },
            updateExpression='SET #index = :val1 modifiedDate = :val2',
            ExpressionAttributeNames={
                '#index': index
            },
            ExpressionAttributeValues={
                ':val1': data,
                ':val2': now.strftime('%Y-%m-%d %H:%M:%S')
            }
        )
    except Exception as e:
        return True, str(e)


def modify_position(_id, types, position, number):
    now = datetime.now(timezone('Asia/Seoul'))
    try:
        response = project_table.scan(FilterExpression=Attr('id').eq(id))['Items'][0]
        wanted = response[types]
        for i in range(0, len(wanted)):
            if wanted[i]['stack'] == position:
                wanted[i]['personal'] = number

        response = project_table.update_item(
            key={
                'id': _id
            },
            updateExpression='SET #type = :val1 modifiedDate = :val2',
            ExpressionAttributeNames={
                '#type': types
            },
            ExpressionAttributeValues={
                ':val1': wanted,
                ':val2': now.strftime('%Y-%m-%d %H:%M:%S')
            }
        )

        return True, response
    except Exception as e:
        return False, str(e)
