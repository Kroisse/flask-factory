# -*- coding: utf-8 -*-
"""flask_factory.factory
~~~~~~~~~~~~~~~~~~~~~

"""
from flask import Flask, current_app
from werkzeug.datastructures import ImmutableDict
from werkzeug.local import LocalProxy

from .initializer import Initializer, BasicInitializer, Extension


def _lookup_ext_instances():
    namespace = current_app.extensions['factory']
    return namespace['ext_instances']


extensions = LocalProxy(_lookup_ext_instances)


class ImmutableNamespace(ImmutableDict):
    def __getattr__(self, item):
        return self[item]


class Factory(object):
    def __init__(self, import_name, cls=Flask, **kwargs):
        self.import_name = import_name
        self.app_cls = cls
        self.app_ctor_kwargs = kwargs
        self._initializers = []

    def _add_extension(self, ext, args, kwargs):
        initializer = Extension(ext, args=args, kwargs=kwargs)
        self._initializers.append(initializer)

        def decorator(f):
            initializer.init_func = f
            return f
        return decorator

    def step(self, initializer, *args, **kwargs):
        additional_args = bool(args or kwargs)
        if isinstance(initializer, Initializer) and not additional_args:
            self._initializers.append(initializer)
            return
        elif callable(initializer) and not additional_args:
            self._initializers.append(BasicInitializer(initializer))
            return initializer
        elif isinstance(initializer, type) and \
                hasattr(initializer, 'init_app'):
            # assume `init` is a Flask extension class
            return self._add_extension(initializer, args, kwargs)
        raise TypeError

    def __call__(self, config=None):
        app = self.app_cls(self.import_name, **self.app_ctor_kwargs)
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        ext_namespace = app.extensions['factory'] = {}
        if config:
            app.config.update(config)
        for i in self._initializers:
            i.init_app(app)
        ext_instances = ext_namespace.get('ext_instances', {})
        ext_namespace['ext_instances'] = ImmutableNamespace(ext_instances)
        return app
