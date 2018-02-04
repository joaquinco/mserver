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
    CORS(app, supports_credentials=True)


def _add_support_engineio_preflights():
    from engineio import Middleware

    Middleware.call_old = Middleware.__call__

    def added_func(instance, environ, start_response):
        """
        If HTTP method is OPTIONS dont call engineio request handler.
        """
        method = environ['REQUEST_METHOD']
        if method == 'OPTIONS':
            return instance.wsgi_app(environ, start_response)
        return instance.call_old(environ, start_response)

    Middleware.__call__ = added_func


def _add_dummy_view_to_expose_socketio_preflights(app):
    """
    Add route that is used only to support OPTIONS in socketio.
    """
    @app.route('/socket.io/', methods=['GET', 'POST'])
    def socketio():
        return ''


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

    import mserver.socket.sockets
    mserver.socket.sockets.on_connect
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


_add_support_engineio_preflights()
app = create_app()
_add_dummy_view_to_expose_socketio_preflights(app)
api = Api(app)
socketio = SocketIO(app)
do_setup(app)
