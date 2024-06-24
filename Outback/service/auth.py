import jwt

from flask import request, jsonify
from flask_bcrypt import generate_password_hash, check_password_hash
from functools import wraps
from datetime import datetime, timedelta

from Outback.config import Config


def hash_password(password):
    return generate_password_hash(password).decode('utf-8')


def verify_password(password, password_hash):
    return check_password_hash(password, password_hash)


def create_token(email):
    payload = {
        'exp': datetime.now() + timedelta(hours=24),  # Token expires in 24 hours
        'iat': datetime.now(),
        'sub': email
    }
    return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')


def decode_token(token):
    try:
        payload = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms='HS256')
        print(payload)
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization']

        if not token:
            return {'message': 'Token is missing!'}, 401

        try:
            sub = decode_token(token)
            print(sub)
            if not sub:
                return {'message': sub}, 401
        except Exception as e:
            return {'message': str(e)}, 401

        return f(sub, *args, **kwargs)

    return decorated
