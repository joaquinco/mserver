from utils.modules import import_submodules, get_current_module

_default_backend = None
_search_backends = {}


def get_default():
    return _default_backend


def get(backend):
    return _search_backends.get(backend)


def register(backend, name=None, set_default=False):
    global _default_backend
    global _search_backends

    if set_default:
        _default_backend = backend
    else:
        assert (name is not None, 'Must provide a name for non default backends')
        _search_backends[name] = backend


import_submodules(get_current_module(__name__))
