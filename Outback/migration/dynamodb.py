import boto3

from Outback.config import Config


dynamodb = boto3.resource(
    'dynamodb',
    region_name=Config.AWS_REGION,
    aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
)

table_name = [table.name for table in dynamodb.tables.all()]
project_table_name = Config.PROJECT_TABLE_NAME
user_table_name = Config.USER_TABLE_NAME
comment_table_name = Config.COMMENT_TABLE


def create_tables():

    if project_table_name not in table_name:
        project_table = dynamodb.create_table(
            TableName=project_table_name,
            KeySchema=[
                {
                    'AttributeName': 'uuid',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'id',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'uuid',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'id',
                    'AttributeType': 'N'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )

    if user_table_name not in table_name:
        user_table = dynamodb.create_table(
            TableName=user_table_name,
            KeySchema=[
                {
                    'AttributeName': 'uuid',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'id',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'uuid',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'id',
                    'AttributeType': 'N'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )

    if comment_table_name not in table_name:
        comment_table = dynamodb.create_table(
            TableName=comment_table_name,
            KeySchema=[
                {
                    'AttributeName': 'uuid',
                    'KeyType': 'HASH'
                },
                {
                    'AttributeName': 'id',
                    'KeyType': 'RANGE'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'uuid',
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': 'id',
                    'AttributeType': 'N'
                }
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )