from __future__ import absolute_import
from importlib import import_module
import pkgutil


NotFound = type('NotFound', (object,), {})()


def import_string(import_name, package=None, default=NotFound):
    try:
        module_name, object_name = import_name.split(':', 1)
    except ValueError:
        module_name = import_name
        object_name = None
    try:
        obj = import_module(module_name, package)
        if object_name:
            obj = getattr(obj, object_name)
        return obj
    except (ImportError, AttributeError):
        if default is not NotFound:
            return default
        raise


def get_nearest_package_name(import_name):
    while True:
        try:
            loader = pkgutil.get_loader(import_name)
            if loader.is_package(import_name):
                return import_name
        except (AttributeError, ImportError):
            return None
        try:
            import_name, _ = import_name.rsplit('.', 1)
        except ValueError:
            return None
