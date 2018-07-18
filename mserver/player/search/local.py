from mserver.models import Song
from mserver.player.mpd import mpd_search
from mserver.player.utils import convert_to_song
from .api import register
from .exceptions import NotFoundError


def local_search(query):
    """
    Searchs songs on local database.
    """
    return list(map(convert_to_song, mpd_search(query)))


def get_song(song_id):
    song = Song.query.filter_by(id=song_id).scalar()

    if not song:
        raise NotFoundError('Song not found')
    return song


register(search=local_search, name='local', set_default=True, get_song=get_song)
