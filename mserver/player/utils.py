def format_int_duration(value):
    """
    Formats an amount of seconds to a hrn duration
    """
    minutes = value // 60
    seconds = value % 60

    return '{min:02}:{sec:02}'.format(min=minutes, sec=seconds)
