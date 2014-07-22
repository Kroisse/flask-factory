# -*- coding: utf-8 -*-
from flask import Flask
from flask_factory import Factory


def test_basic():
    factory = Factory(__name__)
    app = factory()
    assert type(app) == Flask
    assert app.import_name == factory.import_name


def test_with_config():
    config = {'SECRET_KEY': b'wow3very2secret0'}
    factory = Factory(__name__)
    app = factory(config=config)
    assert app.config['SECRET_KEY'] == config['SECRET_KEY']
    config['SECRET_KEY'] = b'not-a-secret-anymore'
    assert app.config['SECRET_KEY'] == b'wow3very2secret0'
