import bcrypt
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


@jwt.jwt_payload_handler
def make_payload(identity):
    return {'user_id': identity.id}
