import re

import pafy
from mserver.models import Song

from .api import register

# TODO: get own api key
api_key = 'AIzaSyCIM4EzNqi1in22f4Z3Ru3iYvLaY8tc3bo'

THIS_SOURCE = 'youtube'

MUSIC_CATEGORYID = 10
ORDER = 'relevance'
VIDEO_DURATION = 'any'

ISO8601_TIMEDUR_EX = re.compile(r'PT((\d{1,3})H)?((\d{1,3})M)?((\d{1,2})S)?')


def generate_search_query(term, category=MUSIC_CATEGORYID, order=ORDER, duration=VIDEO_DURATION, max_results=15):
    qs = {
        'q': term,
        'maxResults': max_results,
        'safeSearch': "none",
        'order': order,
        'part': 'id,snippet',
        'type': 'video',
        'videoDuration': duration,
        'key': api_key,
        'videoCategoryId': category
    }

    return qs


def convert_to_song(item):
    """
    Converts a youtube item to Song object
    """
    pass


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

        current = Song(title=title, duration=duration, source=THIS_SOURCE, available=False, search_id=ytid)
        songs.append(current)

    return songs


def youtube_search(query):
    """
    Searchs songs on youtube.
    """

    qs = generate_search_query(query)

    yresult = pafy.call_gdata('search', qs)

    return get_songs_from_result(yresult)


register(youtube_search, name=THIS_SOURCE)
