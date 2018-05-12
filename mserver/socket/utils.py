from unittest import mock

import flask

from mserver.mserver import socketio
from utils import Dummy


def socket_contexted_async_target(target):
    """
    Mocks flask context to enable emit events in async function calls.

    Must be called within request context.
    """
    request = flask.request
    current_app = flask.current_app
    dummy_request = Dummy(sid=request.sid, namespace=request.namespace)
    dummy_current_app = Dummy(extensions=dict(socketio=current_app.extensions['socketio']))

    def new_target(*args, **kwargs):
        with mock.patch('flask.request', dummy_request):
            with mock.patch('flask.current_app', dummy_current_app):
                return target(*args, **kwargs)

    return new_target


def start_background_task(target, *args, **kwargs):
    # socketio.start_background_task(socket_contexted_async_target(target), *args, **kwargs)
    socketio.start_background_task(target, *args, **kwargs)
