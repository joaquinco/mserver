from utils.modules import import_submodules, get_current_module

_default_backend = None
_search_backends = {}


class _SearchBackend(object):
    def __init__(self, name=None, search_fn=None, get_file_fn=None, get_song_fn=None):
        self._name = name
        self.search_fn = search_fn
        self.get_file_fn = get_file_fn
        self.get_song_fn = get_song_fn

    def search(self, query, *args, **kwargs):
        if hasattr(self.search_fn, '__call__'):
            return self.search_fn(query, *args, **kwargs)
        raise Exception('Search function is not callable')

    def get_file(self, search_id, *args, **kwargs):
        if hasattr(self.get_file_fn, '__call__'):
            return self.get_file_fn(search_id, *args, **kwargs)
        raise Exception('Get file function is not callable')

    def get_song(self, *args, **kwargs):
        if hasattr(self.get_song_fn, '__call__'):
            return self.get_song_fn(*args, **kwargs)
        raise Exception('Get song function is not callable')

    @property
    def name(self):
        return self._name


def get_default():
    return _default_backend


def get(backend):
    return _search_backends.get(backend)


def register(search=None, get_file=None, name=None, set_default=False):
    global _default_backend
    global _search_backends

    backend = _SearchBackend(name=name, search_fn=search, get_file_fn=get_file)

    assert name is not None, 'Must provide a name to serach backend'
    if set_default:
        _default_backend = backend

    _search_backends[name] = backend


import_submodules(get_current_module(__name__))
