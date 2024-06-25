from flask_bcrypt import generate_password_hash, check_password_hash


def hash_password(password):
    return generate_password_hash(password).decode('utf-8')


def verify_password(password, password_hash):
    return check_password_hash(password, password_hash)
