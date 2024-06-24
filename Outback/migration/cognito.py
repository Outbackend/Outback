import boto3

from flask import Flask
from Outback.config import Config


cognito = boto3.client(
    'cognito-idp',
    region_name=Config.AWS_REGION,
    aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
)