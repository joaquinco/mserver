from mserver.models import Song


def format_int_duration(value):
    """
    Formats an amount of seconds to a hrn duration
    """
    minutes = value // 60
    seconds = value % 60

    return '{min:02}:{sec:02}'.format(min=minutes, sec=seconds)


def mpd_convert_to_song(mpd_song, available=True):

    file = mpd_song.get('file')
    time = mpd_song.get('time')
    duration = time and format_int_duration(int(time))

    return Song(id=file, title=file, available=available, duration=duration)
