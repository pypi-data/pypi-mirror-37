import pytest

from antaresia import load
from antaresia import exceptions


def test_travis():
    config = load("examples/travis.ppy")
    assert config == {
        "after_success": ["python-codacy-coverage -r coverage.xml"],
        "install": ["pip install tox tox-travis", "pip install codacy-coverage"],
        "language": "python",
        "python": ["3.6"],
        "script": ["tox"],
    }


def test_travis_fail():
    with pytest.raises(exceptions.MyPyFail):
        load("examples/travis.failmypy.ppy")


def test_expression():
    config = load("examples/expression.ppy")
    assert config == ["foo", "bar"]


def test_import():
    with pytest.raises(exceptions.ForbiddenImport):
        load("examples/import.ppy")
    config = load("examples/import.ppy", allowed_imports=['antaresia.config_functions'])
    assert config == {'imported_var': 54, 'var_1': 7, 'var_2': 2, 'var_3': 42}


def test_timeout():
    with pytest.raises(exceptions.Timeout):
        load("examples/long.ppy", allowed_imports=['time'], timeout=1)
