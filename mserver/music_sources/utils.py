from mserver.models import Song
from mserver import mpd_utils


def update_song_availability(songs, source):
    """
    Given a list of songs, sets them as availables in case they have been already downloaded.
    Also sets the in_playlist attribute to indicate that they are already added to the current playlist.
    """
    ids = [s.search_id for s in songs]

    db_songs = Song.query.filter(Song.search_id.in_(ids)).filter(Song.source == source).all()

    playlist_songs = mpd_utils.playlist()

    db_songs_by_search_id = {s.search_id: s for s in db_songs}

    playlist_songs_by_name = {s.get('file'): s for s in playlist_songs if s.get('file')}

    for song in songs:
        db_song = db_songs_by_search_id.get(song.search_id)
        if db_song:
            song.available = db_song.available

        if song.available:
            playlist_song_name = song.title.endswith('.mp3') and song.title or song.title + '.mp3'

            song.in_playlist = playlist_song_name in playlist_songs_by_name
            if song.in_playlist:
                song.pos = playlist_songs_by_name[playlist_song_name].get('pos')

    return songs
