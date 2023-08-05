from dalloriam.api import API

from unittest import mock


def test_api_initializes_properly():
    a = API('host', 4242, True)
    assert a._host == 'host'
    assert a._port == 4242
    assert a._debug is True