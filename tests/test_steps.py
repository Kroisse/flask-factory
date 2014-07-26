# -*- coding: utf-8 -*-
import pytest
from flask_factory import Factory
from flask_factory.initializer import Extension
from flask_sample import SampleExtension


@pytest.fixture
def create_app():
    return Factory(__name__)


def test_simple_step(create_app):
    @create_app.step
    def modify_jinja_env(app):
        app.jinja_env.globals['site_name'] = "Wonka's Chocolate Factory"

    app = create_app()
    assert app.jinja_env.globals['site_name'] == "Wonka's Chocolate Factory"


def test_initializer_object(create_app):
    create_app.step(Extension(SampleExtension, name='sample_ext'))
    app = create_app()
    assert app.config['SAMPLE_EXTENSION'] == 42


def test_invalid_object(create_app):
    with pytest.raises(TypeError):
        create_app.step(42)
