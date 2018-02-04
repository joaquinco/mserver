from flask_socketio import emit

from .exceptions import MServerException


def handle_exception(error_key):
    """
    Calls method and emit proper error on exception.

    Meant to be used by socket handlers.
    """

    def decorator(wrapped):
        def wrapper(*args, **kwargs):
            try:
                return wrapped(*args, **kwargs)
            except MServerException as e:
                emit('error', {'message': str(e), 'key': error_key})

        return wrapper

    return decorator
