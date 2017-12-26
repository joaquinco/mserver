from sqlalchemy import or_

from mserver.models import Song
from .api import register


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


register(local_search, 'local', set_default=True)
