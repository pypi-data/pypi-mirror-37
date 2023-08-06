# coding=utf-8

from pathlib import Path

import pytest

from elib_config import (
    ConfigValueTableArray, ConfigValueTableKey, ConfigValueTypeError, MissingTableKeyError,
    TableKeyTypeError,
)

_EXAMPLE1 = """
inline_str = { key1= "value1", key2= "other value" } 
"""

_EXAMPLE2 = """
inline_str = {} 
"""


def test_basics():
    Path('config.toml').write_text(_EXAMPLE1)
    key1 = ConfigValueTableKey('key1', str, description='desc')
    inline_str = ConfigValueTableArray('inline_str', description='', keys=(key1,))
    assert {'key1': "value1", 'key2': "other value"} == inline_str()


def test_wrong_key_type():
    Path('config.toml').write_text(_EXAMPLE1)
    key1 = ConfigValueTableKey('key1', int, description='desc')
    inline_str = ConfigValueTableArray('inline_str', description='', keys=(key1,))
    with pytest.raises(TableKeyTypeError):
        inline_str()


def test_missing_key():
    Path('config.toml').write_text(_EXAMPLE1)
    key1 = ConfigValueTableKey('does_not_exist', str, description='desc')
    inline_str = ConfigValueTableArray('inline_str', description='', keys=(key1,))
    with pytest.raises(MissingTableKeyError):
        inline_str()


def test_missing_optional_key():
    Path('config.toml').write_text(_EXAMPLE1)
    key1 = ConfigValueTableKey('does_not_exist', str, description='desc', default='default')
    inline_str = ConfigValueTableArray('inline_str', description='', keys=(key1,))
    assert {'key1': "value1", 'key2': "other value", 'does_not_exist': 'default'} == inline_str()


def test_get_attr():
    Path('config.toml').write_text(_EXAMPLE1)
    key1 = ConfigValueTableKey('key1', str, description='desc')
    inline_str = ConfigValueTableArray('inline_str', description='', keys=(key1,))
    assert 'value1' == inline_str.key1
    assert 'value1' == inline_str['key1']


def test_get_attr_missing():
    Path('config.toml').write_text(_EXAMPLE1)
    key1 = ConfigValueTableKey('key1', str, description='desc')
    inline_str = ConfigValueTableArray('inline_str', description='', keys=(key1,))
    with pytest.raises(AttributeError, match='inline_str: table has no key "key11"'):
        assert 'value1' == inline_str.key11
    with pytest.raises(AttributeError, match='inline_str: table has no key "key11"'):
        assert 'value1' == inline_str['key11']


def test_optional_key():
    Path('config.toml').write_text(_EXAMPLE2)
    key1 = ConfigValueTableKey('key1', str, description='', default='test')
    inline_str = ConfigValueTableArray('inline_str', description='', keys=(key1,))
    assert {'key1': 'test'} == inline_str()


def test_cast_wrong_type():
    key1 = ConfigValueTableKey('key1', str, description='', default='test')
    inline_str = ConfigValueTableArray('inline_str', description='', keys=(key1,))
    with pytest.raises(ConfigValueTypeError):
        inline_str._cast('test')
