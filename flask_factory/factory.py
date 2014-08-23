# -*- coding: utf-8 -*-
"""flask_factory.factory
~~~~~~~~~~~~~~~~~~~~~

"""
from flask import Flask, current_app
from werkzeug.datastructures import ImmutableDict
from werkzeug.local import LocalProxy

from .initializer import Initializer, Action, DeferredAction, Extension


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

    def step(self, initializer):
        if isinstance(initializer, Initializer):
            self._initializers.append(initializer)
        elif isinstance(initializer, str):
            self._initializers.append(DeferredAction(initializer))
        elif callable(initializer):
            self._initializers.append(Action(initializer))
            return initializer
        else:
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
