from app import strtobool
from app.util.strtobool import strtobool_optional


def test_strtobool():
    assert bool(strtobool('y')) is True
    assert bool(strtobool('Yes')) is True
    assert bool(strtobool('t')) is True
    assert bool(strtobool('True')) is True
    assert bool(strtobool('On')) is True
    assert bool(strtobool('1')) is True

    assert bool(strtobool('n')) is False
    assert bool(strtobool('No')) is False
    assert bool(strtobool('f')) is False
    assert bool(strtobool('False')) is False
    assert bool(strtobool('Off')) is False
    assert bool(strtobool('0')) is False


def test_strtobool_optional():
    assert bool(strtobool_optional('True')) is True
    assert bool(strtobool_optional('False')) is False
    assert strtobool_optional(None) is None
    assert strtobool_optional('') is None

