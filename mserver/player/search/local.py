from mserver import mpd_utils
from mserver.player.utils import mpd_convert_to_song
from .api import register
from .exceptions import NotFoundError

THIS_SOURCE = 'local'


def _convert_to_song(data):
    data.update(dict(source=THIS_SOURCE))
    return mpd_convert_to_song(data)


def local_search(query):
    """
    Searches songs on mpd_utils.
    """
    return list(map(_convert_to_song, mpd_utils.search(query)))


def get_song(song_id):
    """
    Obtains a single song.
    """
    song = None

    songs = local_search(song_id)

    if songs:
        song = songs[0]

    if not song:
        raise NotFoundError('Song not found')
    return song


register(search=local_search, name=THIS_SOURCE, set_default=True, get_song=get_song)
