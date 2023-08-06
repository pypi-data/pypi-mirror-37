import pytest
from pytest_bwrap.decorators import network_allowed, read_only

from requests.exceptions import ConnectionError

from . import get_gnome, write_to_file


def test_get_gnome_without_network():
    with pytest.raises(ConnectionError):
        assert get_gnome().status_code == 200


@network_allowed()
def test_get_gnome_with_network():
    assert get_gnome().status_code == 200


def test_write_to_file():
    write_to_file('/tmp/foo/file', 'some text')


def test_write_to_file_in_global_ro_dir():
    with pytest.raises(OSError, message='Read-only file system'):
        write_to_file('/tmp/baz/file', 'some text')


@read_only('/tmp/bar')
def test_write_to_file_in_ro_dir():
    with pytest.raises(OSError, message='Read-only file system'):
        write_to_file('/tmp/bar/file', 'some text')
