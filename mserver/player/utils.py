from mserver.models import DummySong
import copy

def format_int_duration(value):
    """
    Formats an amount of seconds to a hrn duration
    """
    minutes = value // 60
    seconds = value % 60

    return '{min:02}:{sec:02}'.format(min=minutes, sec=seconds)


def mpd_convert_to_song(data, available=True, **kwargs):
    """
    Converts an mpd song result to a mserver Song.
    """
    field_override = ['title']

    mpd_song = copy.deepcopy(data)
    mpd_song.update(kwargs)

    [mpd_song.pop(field, None) for field in field_override]

    file = mpd_song.pop('file')
    time = mpd_song.pop('time', None)
    duration = time and format_int_duration(int(time))

    return DummySong(title=file, available=available, duration=duration, path=file, **mpd_song)
