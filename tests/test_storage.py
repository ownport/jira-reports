
import os
import pytest

from jirareports.storage import Storage


def test_storage_create(tmpdir):

    _path = str(tmpdir.join('storage.sqlite'))
    _storage = Storage(_path)
    assert isinstance(_storage, Storage)


def test_storage_put_and_get(tmpdir):

    _path = str(tmpdir.join('storage.sqlite'))
    _storage = Storage(_path)
    _storage.put('1', **{'k1':'v1', 'k2':'v2'})
    assert _storage.get('1') == {'k1':'v1', 'k2':'v2'}
