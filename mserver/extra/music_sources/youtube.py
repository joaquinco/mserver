import pafy

from mserver.database import db
from mserver.models import Song
from mserver.music_sources import MServerMusicSource
from .youtube_utils import generate_search_query, get_songs_from_result, get_item_info, youtube_download, SOURCE_NAME


class YoutubeSource(MServerMusicSource):
    name = SOURCE_NAME
    readable_name = 'Desde youtube'
    ordering = 10

    def get_song(self, ytid, *args, **kwargs):
        song = db.session.query(Song).filter_by(source=self.name, search_id=ytid).scalar()
        if song:
            return song

        item = get_item_info(ytid)

        snippet = item.get('snippet', {})
        title = snippet.get('title', '').strip()

        return Song(source=self.name, search_id=ytid, title=title)

    def perform_search(self, query, *args, **kwargs):
        """
        Search songs on youtube.
        """
        qs = generate_search_query(query, api_key=self.config.get('api_key'))

        yresult = pafy.call_gdata('search', qs)

        return get_songs_from_result(yresult)

    def get_file(self, ytid, *args, **kwargs):
        """
        Return filename of song.
        """
        return youtube_download(ytid, self.config.get('download_dir'))
