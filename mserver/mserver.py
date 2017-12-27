from collections import OrderedDict

from flask import Flask, jsonify
from flask_jwt import JWTError
from flask_restful import Api

db = None
app = None
api = None


def create_app():
    app = Flask(__name__)
    app.config.from_object('mserver.settings')

    return app


def create_api(app):
    api = Api(app)
    return api


def do_setup(app):
    from .database import init_db
    init_db()

    # global db
    # db = SQLAlchemy()
    # db.init_app(app)

    import mserver.resources
    mserver.resources.SongSearchResource

    import mserver.apiurls
    mserver.apiurls.urls

    import mserver.auth
    mserver.auth.authenticate

    app.handle_user_exception = handle_user_exception_again


def handle_user_exception_again(e):
    if isinstance(e, JWTError):
        return jsonify(OrderedDict([
            ('status_code', e.status_code),
            ('error', e.error),
            ('description', e.description),
        ])), e.status_code, e.headers
    return e


app = create_app()
api = create_api(app)
do_setup(app)
