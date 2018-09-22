import logging

from mpd.base import MPDClient

logger = logging.getLogger('mpd')


def create_mpd_client(*args, **kwargs):
    client = MPDClient(*args, **kwargs)

    _customize(client)

    return client


def _customize(c):
    """
    Add commands to mpd client
    """
    pass
