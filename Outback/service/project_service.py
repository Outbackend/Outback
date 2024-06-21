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
    iid = (dtime * 100000000) + random.randint(10000001, 29999999)
    item = {
        'uuid': str(uuid.uuid4()),
        'id': iid,
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
        'comment': [],
    }
    try:
        response = project_table.put_item(Item=item)
        return True, response
    except Exception as e:
        return False, str(e)


def get_project_by_id(project_id):
    try:
        response = project_table.scan(
            FilterExpression=Attr('id').eq(project_id)
        )
        return True, response['Items'][0]
    except Exception as e:
        return False, str(e)


def get_project_list():
    try:
        response = project_table.scan()
        items = response['Items']
        return True, items
    except Exception as e:
        return False, str(e)


def update_project(_uuid, _id, project):
    now = datetime.now(timezone('Asia/Seoul'))
    try:
        response = project_table.update_item(
            Key={
                'uuid': _uuid,
                'id': _id
            },
            UpdateExpression='SET #t1=:val1, #t2=:val2, #t3=:val3, #t4=:val4, #t5=:val5, #t6=:val6, #t7=:val7, #t8=:val8',
            ExpressionAttributeNames={
                '#t1': 'name',
                '#t2': 'description',
                '#t3': 'stack',
                '#t4': 'wanted',
                '#t5': 'inNow',
                '#t6': 'status',
                '#t7': 'endDate',
                '#t8': 'modifiedDate'
            },
            ExpressionAttributeValues={
                ':val1': project['name'],
                ':val2': project['description'],
                ':val3': project['stack'],
                ':val4': project['wanted'],
                ':val5': project['inNow'],
                ':val6': project['status'],
                ':val7': project['endDate'],
                ':val8': now.strftime('%Y-%m-%d %H:%M:%S'),
            }
        )
        return True, response
    except Exception as e:
        return False, str(e)


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


def delete_project(_uuid, _id):
    try:
        response = project_table.delete_item(
            Key={
                'uuid': _uuid,
                'id': _id
            }
        )
        return True, response
    except Exception as e:
        return False, str(e)


def add_comment(project_uuid, project_id, user_id, parent_id, content):
    now = datetime.now(timezone('Asia/Seoul'))
    dtime = int(time.time() * 1000000)
    uid = str(uuid.uuid4())
    iid = (dtime * 100000000) + random.randint(30000000, 99999999)
    dt = now.strftime('%Y-%m-%d %H:%M:%S')
    comment = {
        'uuid': uid,
        'id': iid,
        'content': content,
        'projectId': project_id,
        'parentId': parent_id,
        'userId': user_id,
        'datetime': dt
    }
    project_comment = {
        'uuid': uid,
        'id': iid,
    }
    try:
        update_response = project_table.update_item(
            Key={
                'uuid': project_uuid,
                'id': project_id
            },
            UpdateExpression='SET #comment = list_append(#comment, :comment)',
            ExpressionAttributeNames={
                '#comment': 'comment'
            },
            ExpressionAttributeValues={
                ':comment': [project_comment]
            },
            ReturnValues='UPDATED_NEW'
        )
        add_response = comment_table.put_item(Item=comment)
        response = {'update_response': update_response, 'add_response': add_response}
        return True, response
    except Exception as e:
        return False, str(e)


def get_comment(_id):
    try:
        response = comment_table.scan(
            FilterExpression=Attr('id').eq(_id)
        )
        return True, response['Items'][0]
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


def update_comment(_uuid, _id, content):
    now = datetime.now(timezone('Asia/Seoul'))
    try:
        comment_response = comment_table.update_item(
            Key={
                'uuid': _uuid,
                'id': _id
            },
            UpdateExpression='SET #content = :content #datetime = :datetime',
            ExpressionAttributeNames={
                '#content': 'content',
                'datetime': 'datetime'
            },
            ExpressionAttributeValues={
                ':content': content,
                ':datetime': now.strftime('%Y-%m-%d %H:%M:%S')
            }
        )
        return True, comment_response
    except Exception as e:
        return False, str(e)


def delete_comment(_uuid, _id):
    try:
        response = comment_table.delete_item(
            Key={
                'uuid': _uuid,
                'id': _id
            }
        )
        return True, response
    except Exception as e:
        return False, str(e)
