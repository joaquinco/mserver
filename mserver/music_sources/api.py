from mserver import settings
from utils.modules import import_object
from .abstract import MServerMusicSource
from .local import LocalSource

CONFIGS = getattr(settings, 'SONG_SOURCES_CONFIG', {})


class _Sources(object):
    sources = {}
    default_source = None
    configs = CONFIGS

    @classmethod
    def add(cls, source_class, is_default=False):
        new_source = source_class(config=cls.configs.get(source_class.name))

        cls.sources[source_class.name] = new_source
        if is_default:
            cls.default_source = new_source

        return new_source

    @classmethod
    def get(cls, name):
        return name and cls.sources.get(name) or cls.default_source

    @classmethod
    def list_info(cls):
        """
        Return list of available sources
        """
        if cls.default_source:
            default_name = cls.default_source.name
        else:
            default_name = None

        return [{'name': s.name, 'is_default': s.name == default_name} for s in cls.sources.values()]

def _validate_source_class(klass):
    """
    Validates music source klass
    """
    if issubclass(klass, MServerMusicSource):
        return

    for attr in filter(lambda x: not x.startswith('_'), dir(MServerMusicSource)):
        if not hasattr(attr, klass):
            raise Exception('{0} has no attribute {1}'.format(repr(klass), attr))


def init_music_sources(source_modules):
    """
    Import source modules which implement a subclass of MServerMusicSource or similar.
    """
    for source_path in source_modules:
        if not hasattr(source_path, '__call__'):
            klass = import_object(source_path)
        else:
            klass = source_path

        _validate_source_class(klass)
        _Sources.add(klass)

    _Sources.add(LocalSource, is_default=True)


def get(source_name=None):
    """
    Return music source.
    """
    return _Sources.get(source_name)


def list_info():
    """
    Return list of available sources
    """
    return _Sources.list_info()