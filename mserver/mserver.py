from collections import OrderedDict

from flask import Flask, jsonify
from flask_jwt import JWTError
from flask_restful import Api
from flask_socketio import SocketIO


def create_app():
    app = Flask(__name__)
    app.config.from_object('mserver.settings')

    return app


def create_api(app):
    api = Api(app)
    return api


def create_and_run_scoketio(app):
    socketio = SocketIO(app)
    socketio.run(app)
    return socketio


def do_setup(app):
    global db
    from .database import init_db
    db = init_db()

    # global db
    # db = SQLAlchemy()
    # db.init_app(app)

    import mserver.resources
    mserver.resources.SongSearchResource

    import mserver.apiurls
    mserver.apiurls.urls

    import mserver.auth
    mserver.auth.authenticate

    import mserver.sockets
    mserver.sockets.on_connect

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
api = create_api(app)
socketio = create_and_run_scoketio(app)
do_setup(app)
