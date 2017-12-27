import bcrypt
from flask import jsonify
from flask_jwt import JWT

from mserver.models import User
from mserver.mserver import app


def authenticate(username, password):
    user = User.query.filter(User.username == username).scalar()
    if user and user.is_superuser:
        if bcrypt.checkpw(password, user.password):
            return user
    else:
        return user


def identify(payload):
    return User.query.filter(User.id == payload['identity']).scalar()


jwt = JWT(app, authenticate, identify)


@jwt.auth_response_handler
def default_auth_response_handler(access_token, identity):
    return jsonify({
        'access_token': access_token.decode('utf-8'),
        'user': {
            'username': identity.username,
            'is_superuser': identity.is_superuser
        }
    })
