from __future__ import absolute_import
from importlib import import_module


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
