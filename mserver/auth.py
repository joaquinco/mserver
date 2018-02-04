import bcrypt
from flask import jsonify
from flask_jwt import JWT

from mserver.database import db
from mserver.models import User
from mserver.mserver import app


def _create_user(username):
    user = User(username=username)
    db.session.add(user)
    db.session.commit()
    return user


def authenticate(username, password):
    user = User.query.filter(User.username == username).scalar()

    if user and user.is_superuser:
        if bcrypt.checkpw(password, user.password):
            return user
    else:
        if not user:
            return _create_user(username)
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
