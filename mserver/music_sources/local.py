from mserver import mpd_utils
from mserver.player.utils import mpd_convert_to_song
from .abstract import MServerMusicSource
from .exceptions import NotFoundError


class LocalSource(MServerMusicSource):
    name = 'local'
    readable_name = 'Disponibles'
    ordering = 1

    def _convert_to_song(self, data):
        data.update(dict(source=self.name, id=data.get('file')))
        return mpd_convert_to_song(data)

    def perform_search(self, query):
        """
        Searches songs in mpd music dir. Excludes songs already added to the playlist.
        """
        playlist_songs = mpd_utils.playlist()

        playlist_songs_by_name = {s.get('file'): s for s in playlist_songs if s.get('file')}

        return list(map(self._convert_to_song,
                        [s for s in mpd_utils.search(query) if s.get('file') not in playlist_songs_by_name]))

    def get_song(self, song_id):
        """
        Obtains a single song.
        """
        song = None

        songs = self.perform_search(song_id)

        if songs:
            song = songs[0]

        if not song:
            raise NotFoundError('Song not found')
        return song
