from mserver.models import Song


def update_song_availability(songs, source):
    """
    Given a list of songs, sets them as availables in case they have been already downloaded.
    """
    ids = [s.search_id for s in songs]

    db_songs = Song.query.filter(Song.search_id.in_(ids)).filter(Song.source == source).all()

    db_songs_by_search_id = {s.search_id: s for s in db_songs}

    for song in songs:
        db_song = db_songs_by_search_id.get(song.search_id)
        if db_song:
            song.available = db_song.available

    return songs
