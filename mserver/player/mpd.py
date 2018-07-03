import datetime
from utils.functional import compose
from mpd import MPDClient

from mserver.settings import MPD_SERVER_CONF


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


def get_status():
    """

    :return:
    """
    with get_client() as conn:
        return normalize_dict(dict(status=conn.status(), stats=conn.stats(), version=conn.mpd_version))
