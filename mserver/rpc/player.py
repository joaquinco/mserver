from .api import register
from mserver.player.search import list_info as get_search_backends_list


def player_sources(*args, **kwargs):
    """
    Returns system information.
    """
    return get_search_backends_list()


register('player-sources', player_sources, secure=True)
