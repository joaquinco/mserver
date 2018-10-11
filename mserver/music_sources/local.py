from mserver import mpd_utils
from mserver.player.utils import mpd_convert_to_song
from .abstract import MServerMusicSource
from .exceptions import NotFoundError


class LocalSource(MServerMusicSource):
    name = 'local'

    def _convert_to_song(self, data):
        data.update(dict(source=self.name))
        return mpd_convert_to_song(data)

    def search(self, query):
        """
        Searches songs on mpd_utils.
        """
        return list(map(self._convert_to_song, mpd_utils.search(query)))

    def get_song(search, song_id):
        """
        Obtains a single song.
        """
        song = None

        songs = search(song_id)

        if songs:
            song = songs[0]

        if not song:
            raise NotFoundError('Song not found')
        return song
