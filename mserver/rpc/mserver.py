from mserver import settings
from .api import register


def system_status(*args, **kwargs):
    """
    Returns system information.
    """
    return {
        'version': settings.VERSION,
        'debug': settings.DEBUG
    }


register('system-status', system_status)
