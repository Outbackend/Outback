import boto3

from flask import Flask
from Outback.config import Config


cognito = boto3.client(
    'cognito-idp'
)
