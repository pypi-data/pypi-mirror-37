# coding=utf-8

import pathlib

import pytest

from elib_config import ConfigMissingValueError, ConfigValueTypeError, ConfigValueString
from elib_config._types import Types


@pytest.fixture(name='value')
def _dummy_string_value():
    yield ConfigValueString(
        'key',
        description='desc',
        default='default',
    )


def test_no_default():
    value = ConfigValueString(
        'test', 'value',
        description='test',
    )
    with pytest.raises(ConfigMissingValueError):
        value()


def test_string_value_default(value):
    assert value() == 'default'


def test_string_value_type_name(value):
    assert value.type_name == Types.string


@pytest.mark.parametrize(
    'file_value',
    [
        10,
        'true',
        '["some", "list"]',
        '{some = "dict"}',
    ]
)
def test_invalid_cast_type_from_config_file(value, file_value):
    pathlib.Path('config.toml').write_text(f'key = {file_value}')
    exc_msg = f'{value.name}: config value must be of type "string", got .* instead'
    with pytest.raises(ConfigValueTypeError, match=exc_msg):
        value()


def test_valid_cast_type_from_config_file(value):
    pathlib.Path('config.toml').write_text(f'key = "some string"')
    assert value() == 'some string'
    assert isinstance(value(), str)


def test_valid_cast_type_from_config_file_single_quotes(value):
    pathlib.Path('config.toml').write_text(f'key = \'some string\'')
    assert value() == 'some string'
    assert isinstance(value(), str)
