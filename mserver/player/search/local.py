from mserver.player.mpd import mpd_search
from mserver.player.utils import mpd_convert_to_song
from .api import register
from .exceptions import NotFoundError


def local_search(query):
    """
    Searches songs on mpd.
    """
    return list(map(mpd_convert_to_song, mpd_search(query)))


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


register(search=local_search, name='local', set_default=True, get_song=get_song)
