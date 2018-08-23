import logging
import os
from collections import OrderedDict
from functools import partial
from logging.handlers import RotatingFileHandler

import eventlet
from celery import Celery
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt import JWTError
from flask_restful import Api
from flask_socketio import SocketIO

from mserver import settings


def create_app():
    app = Flask(__name__, template_folder='../dist', static_folder='../dist/static')
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


def setup_logging(app):
    """Configures logging"""

    get_log_file = partial(os.path.join, settings.LOG_DIR)

    root = logging.getLogger()
    root.addHandler(RotatingFileHandler(get_log_file('general.log')))
    root.setLevel(settings.LOG_LEVEL)

    for entry in settings.LOGGERS:
        logger = logging.getLogger(entry)
        logger.addHandler(RotatingFileHandler(get_log_file('{0}.log'.format(entry))))
        logger.setLevel(settings.LOG_LEVEL)

    app.logger.addHandler(RotatingFileHandler(get_log_file('mserver.log')))
    app.logger.setLevel(settings.LOG_LEVEL)


def do_setup(app):
    from .database import init_db
    init_db()
    setup_cors(app)
    setup_logging(app)

    import mserver.resources
    mserver.resources.SongSearchResource

    import mserver.apiurls
    mserver.apiurls.urls

    import mserver.auth
    mserver.auth.authenticate

    import mserver.socket_server.handlers
    mserver.socket_server.handlers.on_connect

    import mserver.views
    mserver.views.index

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


def get_socketio(app=None):
    kwargs = dict(message_queue=settings.SOCKETIO_REDIS_URL)
    if app:
        kwargs['async_mode'] = app.config['SOCKETIO_ASYNC_MODE']
    return SocketIO(app, **kwargs)


def get_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


_add_support_engineio_preflights()
app = create_app()
_add_dummy_view_to_expose_socketio_preflights(app)
api = Api(app)
socketio = get_socketio(app)

celery = get_celery(app)

do_setup(app)


def run_server():
    eventlet.monkey_patch()
    socketio.run(app, host='0.0.0.0')
