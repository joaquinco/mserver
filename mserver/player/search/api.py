from utils.modules import import_submodules, get_current_module

_default_backend = None
_search_backends = {}


class _SearchBackend(object):
    def __init__(self, name=None, search_fn=None):
        self._name = name
        self.search_fn = search_fn

    def search(self, query, *args, **kwargs):
        if hasattr(self.search_fn, '__call__'):
            return self.search_fn(query, *args, **kwargs)
        raise Exception('Search function is not callable')

    @property
    def name(self):
        return self._name


def get_default():
    return _default_backend


def get(backend):
    return _search_backends.get(backend)


def register(search_fn, name=None, set_default=False):
    global _default_backend
    global _search_backends

    backend = _SearchBackend(name=name, search_fn=search_fn)

    assert name is not None, 'Must provide a name to serach backend'
    if set_default:
        _default_backend = backend

    _search_backends[name] = backend


import_submodules(get_current_module(__name__))
