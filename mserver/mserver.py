from collections import OrderedDict

from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt import JWTError
from flask_restful import Api
from flask_socketio import SocketIO


def create_app():
    app = Flask(__name__)
    app.config.from_object('mserver.settings')

    return app


def setup_cors(app):
    CORS(app)


def do_setup(app):
    from .database import init_db
    init_db()
    setup_cors(app)

    import mserver.resources
    mserver.resources.SongSearchResource

    import mserver.apiurls
    mserver.apiurls.urls

    import mserver.auth
    mserver.auth.authenticate

    import mserver.sockets
    mserver.sockets.on_connect
    socketio.run(app)

    app.handle_user_exception = handle_user_exception_again


def handle_user_exception_again(e):
    """
    Handles exceptions raised by flask-jwt within flask-restfull views
    """
    if isinstance(e, JWTError):
        return jsonify(OrderedDict([
            ('status_code', e.status_code),
            ('error', e.error),
            ('description', e.description),
        ])), e.status_code, e.headers
    return e


app = create_app()
api = Api(app)
socketio = SocketIO(app, cors_allowed_origins='*', cors_credentials=True)
do_setup(app)
