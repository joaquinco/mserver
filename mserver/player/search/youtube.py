import os
import re
import subprocess
from string import Template

import pafy

from mserver import settings
from mserver.database import db
from mserver.models import Song
from mserver.player.utils import format_int_duration
from .api import register
from .exceptions import DownloadError

THIS_SOURCE = 'youtube'

CONFIG = settings.SONG_SOURCES_CONFIG.get(THIS_SOURCE, {})

API_KEY = CONFIG.get('api_key')

MUSIC_CATEGORYID = 10
ORDER = 'relevance'
VIDEO_DURATION = 'medium'  # ('any', 'short', 'medium', 'long')
AUDIO_FORMAT = 'mp3'
AUDIO_FORMAT_EXTENSION = 'mp3'

ISO8601_TIMEDUR_EX = re.compile(r'PT((\d{1,3})H)?((\d{1,3})M)?((\d{1,2})S)?')

VIDEO_URL_TEMPLATE = Template('https://www.youtube.com/watch?v=$ytid')


def generate_search_query(term, category=MUSIC_CATEGORYID, order=ORDER, duration=VIDEO_DURATION, max_results=15):
    qs = {
        'q': term,
        'maxResults': max_results,
        'safeSearch': "none",
        'order': order,
        'part': 'id,snippet',
        'type': 'video',
        'videoDuration': duration,
        'key': API_KEY,
        'videoCategoryId': category
    }

    return qs


def get_track_id_from_json(item):
    """ Try to extract video Id from various response types """
    fields = ['contentDetails/videoId',
              'snippet/resourceId/videoId',
              'id/videoId',
              'id']
    for field in fields:
        node = item
        for p in field.split('/'):
            if node and isinstance(node, dict):
                node = node.get(p)
        if node:
            return node
    return ''


def get_duration_from_duration(duration):
    """
    Return duration in seconds from youtube duration.
    """
    if duration:
        duration = ISO8601_TIMEDUR_EX.findall(duration)
        if len(duration) > 0:
            _, hours, _, minutes, _, seconds = duration[0]
            duration = [seconds, minutes, hours]
            duration = [int(v) if len(v) > 0 else 0 for v in duration]
            duration = sum([60 ** p * v for p, v in enumerate(duration)])
        else:
            duration = 30
    else:
        duration = 30

    return duration


def get_songs_from_result(yresult):
    """
    Return items from youtube search result
    """
    items = yresult.get("items")
    if not items:
        # TODO: logger
        print('Result withou items')
        return ()

    # fetch detailed information about items from videos API
    id_list = [get_track_id_from_json(i)
               for i in items
               if i['id']['kind'] == 'youtube#video']

    qs = {'part': 'contentDetails,statistics,snippet',
          'id': ','.join(id_list)}

    wdata = pafy.call_gdata('videos', qs)

    items_vidinfo = wdata.get('items', [])
    # enhance search results by adding information from videos API response
    for searchresult, vidinfoitem in zip(items, items_vidinfo):
        searchresult.update(vidinfoitem)

    # populate list of video objects
    songs = []
    for item in items:
        ytid = get_track_id_from_json(item)
        duration = item.get('contentDetails', {}).get('duration')
        duration = get_duration_from_duration(duration)

        snippet = item.get('snippet', {})
        title = snippet.get('title', '').strip()

        duration = format_int_duration(duration)

        current = Song(title=title, duration=duration, source=THIS_SOURCE, available=False, search_id=ytid)
        songs.append(current)

    return songs


def youtube_search(query):
    """
    Search songs on youtube.
    """
    qs = generate_search_query(query)

    yresult = pafy.call_gdata('search', qs)

    return update_song_availability(get_songs_from_result(yresult))


def update_song_availability(songs):
    """
    Given a list of songs, sets them as availables in case they have been already downloaded.
    """
    ids = [s.search_id for s in songs]

    db_songs = Song.query.filter(Song.search_id.in_(ids)).all()

    db_songs_by_search_id = {s.search_id: s for s in db_songs}

    for song in songs:
        db_song = db_songs_by_search_id.get(song.search_id)
        song.available = db_song and db_song.available

    return songs


def get_download_cmd(ytid, filename, audio_format=AUDIO_FORMAT):
    """
    Returns download command
    """
    url = VIDEO_URL_TEMPLATE.substitute(ytid=ytid)
    return ['youtube-dl', '-x', '--audio-format', audio_format, '-o', filename, url]


def get_item_info(ytid):
    """
    Fetchs data from single item from youtube
    """
    qs = {'part': 'contentDetails,statistics,snippet',
          'id': ','.join([ytid])}

    wdata = pafy.call_gdata('videos', qs)
    items_vidinfo = wdata.get('items', [])

    return items_vidinfo[0] if items_vidinfo else {}


def get_song_from_ytid(ytid):
    """
    Returns Song instance from ytid with basic fields filed
    """
    song = db.session.query(Song).filter_by(source=THIS_SOURCE, search_id=ytid).scalar()
    if song:
        return song

    item = get_item_info(ytid)

    snippet = item.get('snippet', {})
    title = snippet.get('title', '').strip()

    return Song(source=THIS_SOURCE, search_id=ytid, title=title)


def youtube_download(search_id):
    """
    Download content from youtube.
    """
    download_dir = settings.MUSIC_DIR

    item = get_item_info(search_id)

    snippet = item.get('snippet', {})
    title = snippet.get('title', '').strip()

    filename_base = os.path.join(download_dir, title)
    filename = '{0}.{1}'.format(filename_base, AUDIO_FORMAT_EXTENSION)

    youtube_dl_output = '{0}.%(ext)s'.format(filename_base)

    if not os.path.exists(filename):
        cmd = get_download_cmd(search_id, youtube_dl_output, audio_format=AUDIO_FORMAT)
        exitcode = subprocess.call(cmd)
        if exitcode != 0:
            raise DownloadError('Error downloading search_id={0} from source {1}'.format(search_id, THIS_SOURCE))

    basename = os.path.basename(filename)

    return basename


register(search=youtube_search, get_song=get_song_from_ytid, get_file=youtube_download, name=THIS_SOURCE)
