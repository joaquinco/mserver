from mserver.player.mpd import mpd_get_status
from mserver.player.search import list_info as get_search_backends_list
from .api import register


def player_status(*args, **kwargs):
    """
    Returns player current information.
    """
    return mpd_get_status()


def player_sources(*args, **kwargs):
    """
    Returns system information.
    """
    return get_search_backends_list()


register('player-sources', player_sources, secure=True)
register('player-status', player_status, secure=True)
