import pytest
import types
from flask_factory.utils import import_string


def test_import_module_by_string():
    with pytest.raises(ImportError):
        import_string('not_existing')
    m = import_string('.mod', 'pkg')
    assert isinstance(m, types.ModuleType)
    assert m.__name__ == 'pkg.mod'


def test_import_object_by_string():
    answer = import_string('pkg.mod:answer')
    assert answer == 42
    widget = import_string('.mod:Widget', 'pkg')
    assert isinstance(widget, type)
    assert widget.__module__ == 'pkg.mod'


def test_import_default():
    m = import_string('not_existing', default=None)
    assert m is None
