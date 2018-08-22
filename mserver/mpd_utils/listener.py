import logging

from mserver.mpd_utils.api import get_client


logger = logging.getLogger('mpd_listener')


def listen_events(subsystems, event_handler):
    """
    Listen MPD events
    """
    logger.info('MPD Listener::Starting')

    mpds = get_client()

    mpds.connect()

    listen_subsystems = subsystems

    while True:
        events = mpds.idle(*listen_subsystems)

        logger.debug('MPD Listener::Events: {0}'.format(', '.join(events)))

        for event in events:
            event_handler(event)
