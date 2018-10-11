class MServerMusicSource(object):
    name = None

    def __init__(self, *args, **kwargs):
        self.config = kwargs.pop('config')


    def get_song(self, *args, **kwargs):
        """
        Return Song like object
        """
        raise NotImplementedError()

    def search(self, *args, **kwargs):
        """
        Return song list according to search params.
        """
        raise NotImplementedError()

    def get_file(self, *args, **kwargs):
        """
        Return filename of song.
        """
        raise NotImplementedError()