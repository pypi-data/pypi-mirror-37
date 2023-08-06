
import pytest
from pyerepfit.utils import *
from unittest.mock import patch

@pytest.mark.parametrize("value, unit, expected", [
    (627.50947415, 'kcal/mol', 1.0),
    (1.0, 'h', 1.0),
    (27.211386, 'ev', 1.0),
    (pytest.param(2.0, 'Ry', 1.0, marks=[pytest.mark.xfail(raises=ValueError)]))
])
def test_get_energy_in_au(value, unit, expected):
    assert get_energy_in_au(value, unit) == pytest.approx(expected)

@pytest.mark.parametrize("value, unit, expected", [
    (1.0, 'bohr', 1.0),
    (0.529177, 'aa', 1.0),
    (pytest.param(2.0, 'cm', 1.0, marks=[pytest.mark.xfail(raises=ValueError)]))
])
def test_get_length_in_au(value, unit, expected):
    assert get_length_in_au(value, unit) == pytest.approx(expected)

@pytest.mark.parametrize("expected, unit, value", [
    (627.50947415, 'kcal/mol', 1.0),
    (1.0, 'h', 1.0),
    (27.211386, 'ev', 1.0),
    (pytest.param(2.0, 'Ry', 1.0, marks=[pytest.mark.xfail(raises=ValueError)]))
])
def test_get_energy_from_au(value, unit, expected):
    assert get_energy_from_au(value, unit) == pytest.approx(expected)

def myexists(path):
    return True

def myexists2(path):
    if (path.startswith('/def')):
        return True
    return False

def myexists3(path):
    return False


def test_which(monkeypatch):
    with monkeypatch.context() as m:
        m.setenv('PATH', '/abc:/def')
        m.setattr(os.path, 'exists', myexists)
        assert which('ala') == '/abc/ala'

def test_which2(monkeypatch):
    with monkeypatch.context() as m:
        m.setenv('PATH', '/abc:/def')
        m.setattr(os.path, 'exists', myexists2)
        assert which('ala') == '/def/ala'

def test_which3(monkeypatch):
    with monkeypatch.context() as m:
        m.setattr(os.path, 'exists', myexists3)
        assert which('ala') == 'ala'
    
