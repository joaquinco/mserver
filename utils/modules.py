def import_submodules(package_name):
    import sys
    import importlib
    import pkgutil
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


def get_current_module(name):
    """
    Returns current module if its not called from __init__.
    """
    return '.'.join(name.split('.')[:-1])
