import datetime

from mpd import MPDClient

from mserver.settings import MPD_SERVER_CONF
from utils.functional import compose


def _mpd_bool(value):
    return {'0': False, '1': True}.get(value)


_key_transform = {
    'db_update': compose(int, datetime.datetime.fromtimestamp, lambda x: x.isoformat()),
    'random': _mpd_bool,
    'repeat': _mpd_bool,
    'single': _mpd_bool,
    'consume': _mpd_bool
}


def normalize(key, value):
    """
    Normalize mpd values to python
    """
    if isinstance(value, dict):
        return normalize_dict(value)
    try:
        return _key_transform.get(key, lambda x: x)(value)
    except Exception as e:
        return None


def normalize_dict(data):
    return {k: normalize(k, v) for (k, v) in data.items()}


def normalize_mpd_response(method):
    def wrapper(*args, **kwargs):
        return normalize_dict(method(*args, **kwargs))

    return wrapper


class _MPDClientWrapper(object):
    def __init__(self, *args, **kwargs):
        self.client = MPDClient(*args, **kwargs)

    def __enter__(self):
        self.client.connect(MPD_SERVER_CONF.get('host'), MPD_SERVER_CONF.get('post'))
        return self.client

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
        self.client.disconnect()


def get_client():
    """
    Returns client to comunicate with mpd
    """
    return _MPDClientWrapper()


@normalize_mpd_response
def mpd_get_status():
    """
    Get mpd current status.
    """
    with get_client() as conn:
        return dict(status=conn.status(), stats=conn.stats(), version=conn.mpd_version)


def mpd_get_playlist():
    """
    Returns songs of current playlist.

    Each song is {'file': 'File name'}
    """
    with get_client() as conn:
        return conn.listall()


@normalize_mpd_response
def mpd_play():
    """
    Continue or start playing

    Return player status
    """
    with get_client() as conn:
        conn.play()

        return conn.status()


@normalize_mpd_response
def mpd_pause():
    """
    Stops playing.

    Return player status
    """
    with get_client() as conn:
        conn.pause()

        return conn.status()
