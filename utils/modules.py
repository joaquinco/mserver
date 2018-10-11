import importlib
import pkgutil
import sys

from .functional import compose


def import_submodules(package_name):
    """ Import all submodules of a module, recursively

    :param package_name: Package name
    :type package_name: str
    :rtype: dict[types.ModuleType]
    """
    package = sys.modules[package_name]
    return {
        name: importlib.import_module(package_name + '.' + name)
        for loader, name, is_pkg in pkgutil.walk_packages(package.__path__)
    }


def get_module_from_full_path(name):
    """
    Returns current module if its not called from __init__.
    """
    return '.'.join(name.split('.')[:-1])


import_current_module_submodules = compose(get_module_from_full_path, import_submodules)


def import_object(full_name):
    """
    Import object from full python path.
    """
    object_name = full_name.split('.')[-1]
    module_name = get_module_from_full_path(full_name)
    module = importlib.import_module(module_name)

    if not hasattr(module, object_name):
        return Exception('Cannot find module {0}'.format(full_name))

    return getattr(module, object_name)
