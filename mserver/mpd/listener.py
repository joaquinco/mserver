from mserver.mpd.api import get_client


def listen_events(subsystems, event_handler):
    """
    Listen MPD events
    """
    mpds = get_client()

    mpds.connect()

    listen_subsystems = subsystems

    while True:
        events = mpds.idle(*listen_subsystems)

        for event in events:
            event_handler(event)
