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
        self.client.connect(MPD_SERVER_CONF.get('host'), MPD_SERVER_CONF.get('port'))
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
        ret = []
        for index, item in enumerate(conn._parse_database(conn.playlist())):
            item['pos'] = index
            ret.append(item)

        return ret


def mpd_add_song_to_db(file):
    """
    Adds song to mpd's song db
    """
    with get_client() as conn:
        conn.update(file)


def mpd_add_song(file):
    """
    Adds song to current playlist
    """
    with get_client() as conn:
        conn.add(file)


@normalize_mpd_response
def mpd_play():
    """
    Continue or start playing

    Return player status
    """
    with get_client() as conn:
        conn.play()
        return conn.status()


def mpd_select(pos):
    """
    Starts playing song at :pos
    """
    with get_client() as conn:
        conn.play(pos)


@normalize_mpd_response
def mpd_pause():
    """
    Stops playing.

    Return player status
    """
    with get_client() as conn:
        conn.pause()
        return conn.status()


def mpd_next():
    """
    Play next song
    """
    with get_client() as conn:
        conn.next()


def mpd_previous():
    """
    Play previous song
    """
    with get_client() as conn:
        conn.previous()


def mpd_get_current():
    """
    Get current song
    """
    with get_client() as conn:
        return conn.currentsong()


def mpd_search(query):
    """
    Performs a search over mpd database
    """
    with get_client() as conn:
        return conn.search('file', query)


def mpd_random(value):
    """
    Activates/deactivates random
    """
    with get_client() as conn:
        conn.random(value and 1 or 0)


def mpd_repeat(value):
    """
    Activetes/deactivate repeat
    """
    with get_client() as conn:
        conn.repeat(value and 1 or 0)
