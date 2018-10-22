from .utils import update_song_availability


class MServerMusicSource(object):
    name = None

    def __init__(self, *args, **kwargs):
        self.config = kwargs.pop('config', {})

    def get_song(self, *args, **kwargs):
        """
        Return Song like object
        """
        raise NotImplementedError()

    def perform_search(self, *args, **kwargs):
        """
        Return song list according to search params.
        """
        raise NotImplementedError()

    def get_file(self, *args, **kwargs):
        """
        Return filename of song.
        """
        raise NotImplementedError()

    def search(self, *args, **kwargs):
        """
        Entry point to search
        """
        songs = self.perform_search(*args, **kwargs)

        return update_song_availability(songs)
