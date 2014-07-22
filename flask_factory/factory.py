# -*- coding: utf-8 -*-
"""flask.ext.factory.factory
~~~~~~~~~~~~~~~~~~~~~~~~~

"""
import logging
from flask import Flask, current_app
from werkzeug.datastructures import ImmutableDict
from werkzeug.local import LocalProxy


def _lookup_ext_instances():
    namespace = current_app.extensions['factory']
    return namespace['ext_instances']


extensions = LocalProxy(_lookup_ext_instances)


def discover_ext_name(name):
    """

    :param name:
    :return:

    >>> discover_ext_name('flask_sqlite3.base')
    'sqlite3'
    >>> discover_ext_name('flask_mongokit')
    'mongokit'

    """
    top_level_pkg_name = name.split('.', 1)[0]
    prefix, ext_name = top_level_pkg_name.split('_', 1)
    assert prefix == 'flask'
    return ext_name


class ImmutableNamespace(ImmutableDict):
    def __getattr__(self, item):
        return self[item]


class Factory(object):
    def __init__(self, import_name, cls=Flask, **kwargs):
        self.import_name = import_name
        self.app_cls = cls
        self.app_ctor_kwargs = kwargs
        self._init_funcs = []

    def add_extension(self, ext, *args, **kwargs):
        index = len(self._init_funcs)
        self._init_funcs.append({
            'type': 'ext',
            'ext_cls': ext,
            'ext_init_params': (args, kwargs),
            'func': None,
        })

        def decorator(f):
            self._init_funcs[index]['func'] = f
            return f
        return decorator

    def add_initializer(self, f):
        self._init_funcs.append({'type': 'init', 'func': f})
        return f

    def __call__(self, config=None):
        app = self.app_cls(self.import_name, **self.app_ctor_kwargs)
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        ext_namespace = app.extensions['factory'] = {}
        if config:
            app.config.update(config)
        ext_instances = {}
        for i in self._init_funcs:
            ty = i['type']
            if ty == 'init':
                i['func'](app)
            elif ty == 'ext':
                ext_cls = i['ext_cls']
                args, kwargs = i['ext_init_params']
                inst = ext_cls(app, *args, **kwargs)
                inst.init_app(app)
                f = i.get('func')
                if callable(f):
                    f(app, inst)
                ext_name = discover_ext_name(ext_cls.__module__)
                ext_instances[ext_name] = inst
            else:
                log = logging.getLogger(__name__ + '.Factory.__call__')
                log.debug('Invalid data: %r', i)
                raise RuntimeError()
        ext_namespace['ext_instances'] = ImmutableNamespace(ext_instances)
        return app
