import datetime

from .client import MServerMPDClient

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


def _normalize(key, value):
    """
    Normalize mpd_utils values to python
    """
    if isinstance(value, dict):
        return _normalize_dict(value)
    try:
        return _key_transform.get(key, lambda x: x)(value)
    except Exception as e:
        return None


def _normalize_dict(data):
    return {k: _normalize(k, v) for (k, v) in data.items()}


def _normalize_mpd_response(method):
    def wrapper(*args, **kwargs):
        return _normalize_dict(method(*args, **kwargs))

    return wrapper


class _MPDClientWrapper(object):
    def __init__(self, *args, **kwargs):
        self.client = MServerMPDClient(*args, **kwargs)

    def connect(self):
        self.client.connect(MPD_SERVER_CONF.get('host'), MPD_SERVER_CONF.get('port'))

    def __enter__(self):
        self.connect()
        return self.client

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
        self.client.disconnect()

    def __getattr__(self, item):
        return getattr(self.client, item)


def get_client():
    """
    Returns client to comunicate with mpd_utils
    """
    return _MPDClientWrapper()


def _with_mpd_client(method):
    def mpd_client_wrapped(*args, **kwargs):
        with get_client() as conn:
            return method(conn, *args, **kwargs)

    return mpd_client_wrapped


@_normalize_mpd_response
@_with_mpd_client
def status(conn):
    """
    Get mpd_utils current status.
    """
    return dict(status=conn.status(), stats=conn.stats(), version=conn.mpd_version)


@_with_mpd_client
def playlist(conn):
    """
    Returns songs of current playlist.

    Each song is {'file': 'File name'}
    """
    ret = []
    for index, item in enumerate(conn._parse_database(conn.playlist())):
        item['pos'] = index
        ret.append(item)

    return ret


@_with_mpd_client
def update(conn, uri):
    """
    Adds song to mpd_utils's song db
    """
    conn.update(uri)


@_with_mpd_client
def add(conn, file):
    """
    Adds song to current playlist
    """
    conn.add(file)


@_with_mpd_client
def play(conn, pos=None):
    """
    Continue or start playing

    Return player status
    """
    if pos is None:
        conn.play()
    else:
        conn.play(pos)


@_with_mpd_client
def pause(conn):
    """
    Stops playing.

    Return player status
    """
    conn.pause()


@_with_mpd_client
def next(conn):
    """
    Play next song
    """
    conn.next()


@_with_mpd_client
def previous(conn):
    """
    Play previous song
    """
    conn.previous()


@_with_mpd_client
def currentsong(conn):
    """
    Get current song
    """
    return conn.currentsong()


@_with_mpd_client
def search(conn, query):
    """
    Performs a search over mpd_utils database
    """
    return conn.search('file', query)


@_with_mpd_client
def random(conn, value):
    """
    Activates/deactivates random
    """
    conn.random(value and 1 or 0)


@_with_mpd_client
def repeat(conn, value):
    """
    Activetes/deactivate repeat
    """
    conn.repeat(value and 1 or 0)


@_with_mpd_client
def delete(conn, pos):
    """
    Deletes song from playlist
    """
    conn.delete(pos)


@_with_mpd_client
def setvol(conn, vol):
    """Sets volume"""
    conn.setvol(vol)


@_with_mpd_client
def cmd(conn, cmd_name, *args):
    """Calls arbitrary command"""
    return getattr(conn, cmd_name)(*args)
