from .utils import update_song_availability


class MServerMusicSource(object):
    # Internal reference name
    name = None
    # Displayed name
    readable_name = None
    # Ordering when showing it in FE. Lower is more to the top.
    ordering = 0

    def __init__(self, *args, **kwargs):
        self.config = kwargs.pop('config', {})

    def to_dict(self):
        return {k: getattr(self, k) for k in ['name', 'ordering', 'readable_name']}

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

        return update_song_availability(songs, self.name)
