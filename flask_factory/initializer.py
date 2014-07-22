# -*- coding: utf-8 -*-
from abc import ABCMeta, abstractmethod

from flask._compat import with_metaclass


__all__ = ['Initializer', 'Extension']


class Initializer(with_metaclass(ABCMeta)):
    @abstractmethod
    def init_app(self, app):
        raise NotImplementedError


class BasicInitializer(Initializer):
    def __init__(self, f):
        self._func = f

    def init_app(self, app):
        self._func(app)


class Extension(Initializer):
    def __init__(self, ext_cls, name=None, args=(), kwargs=None,
                 init_func=None):
        self.ext_cls = ext_cls
        if name is None:
            name = discover_ext_name(ext_cls.__module__)
        self.ext_name = name
        self.init_args = args
        self.init_kwargs = kwargs or {}
        self.init_func = init_func

    def init_app(self, app):
        inst = self.ext_cls(app, *self.init_args, **self.init_kwargs)
        if callable(self.init_func):
            self.init_func(app, inst)
        ext_instances = app.extensions['factory'] \
                           .setdefault('ext_instances', {})
        ext_instances[self.ext_name] = inst


def discover_ext_name(name):
    """

    :param name:
    :return:

    >>> discover_ext_name('flask_sqlite3.base')
    'sqlite3'
    >>> discover_ext_name('flask_mongokit')
    'mongokit'
    >>> discover_ext_name('flask.ext.sqlalchemy._compat')
    'sqlalchemy'
    >>> discover_ext_name('flaskext.login')
    'login'

    """
    if name.startswith('flask_'):
        top_level_pkg_name = name.split('.', 1)[0]
        prefix, ext_name = top_level_pkg_name.split('_', 1)
        return ext_name
    elif name.startswith('flask.ext.'):
        mod_path = name.split('.', 3)
        ext_name = mod_path[2]
        return ext_name
    elif name.startswith('flaskext.'):
        mod_path = name.split('.', 2)
        ext_name = mod_path[1]
        return ext_name
    else:
        raise ValueError(name)
