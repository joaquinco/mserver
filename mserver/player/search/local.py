from sqlalchemy import or_

from mserver.models import Song
from .api import register
from .exceptions import NotFoundError


def local_search(query):
    """
    Searchs songs on local database.
    """
    like_query = '%{0}%'.format(query)
    return Song.query.filter(or_(
        Song.title.ilike(like_query),
        Song.artist.ilike(like_query),
        Song.album.ilike(like_query)
    )).all()


def get_song(song_id):
    song = Song.query.filter_by(id=song_id).scalar()

    if not song:
        raise NotFoundError('Song not found')
    return song


register(search=local_search, name='local', set_default=True, get_song=get_song)
