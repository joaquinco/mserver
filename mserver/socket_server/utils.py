import json

from flask import request
from flask_socketio import emit as socketio_emit

from mserver.application import socketio


def _stringify_data(kwargs):
    """
    If data is dict json.dumps it
    """

    data = kwargs.get('data', None)
    if data and isinstance(data, dict):
        data = json.dumps(data)
        kwargs['data'] = data

    return kwargs


def emit(*args, **kwargs):
    """
    Calls proper emit function depending on request context
    """
    broadcast = kwargs.get('broadcast', False)

    if broadcast or not request:
        socketio.emit(*args, **kwargs)
    else:
        socketio_emit(*args, **kwargs)
