import json

from mserver.mserver import socketio


def start_background_task(target, *args, **kwargs):
    # socketio.start_background_task(socket_contexted_async_target(target), *args, **kwargs)
    socketio.start_background_task(target, *args, **kwargs)


def _stringify_data(kwargs):
    """
    If data is dict json.dumps it
    """

    data = kwargs.get('data', None)
    if data and isinstance(data, dict):
        data = json.dumps(data)
        kwargs['data'] = data

    return kwargs
