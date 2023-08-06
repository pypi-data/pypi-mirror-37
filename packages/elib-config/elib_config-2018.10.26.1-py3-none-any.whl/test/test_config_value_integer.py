# coding=utf-8

import pathlib

import pytest

from elib_config import ConfigMissingValueError, ConfigValueTypeError, ConfigValueInteger, OutOfBoundError


@pytest.fixture(name='value')
def _dummy_string_value():
    yield ConfigValueInteger(
        'key',
        description='desc',
        default=10,
    )


def test_no_default():
    value = ConfigValueInteger(
        'test', 'value',
        description='test',
    )
    with pytest.raises(ConfigMissingValueError):
        value()


def test_string_value_default(value):
    assert value() is 10


def test_string_value_type_name(value):
    assert value.type_name == 'integer'


@pytest.mark.parametrize(
    'file_value',
    [
        '"string"',
        '"10"',
        'true',
        '["some", "list"]',
        '{some = "dict"}',
    ]
)
def test_invalid_cast_type_from_config_file(value, file_value):
    pathlib.Path('config.toml').write_text(f'key = {file_value}')
    exc_msg = f'{value.name}: config value must be of type "integer", got .* instead'
    with pytest.raises(ConfigValueTypeError, match=exc_msg):
        value()


def test_valid_cast_type_from_config_file(value):
    pathlib.Path('config.toml').write_text(f'key = 5')
    assert value() is 5


def test_min(value: ConfigValueInteger):
    assert value() is 10
    value.set_limits(min_=10)
    assert value() is 10
    value.set_limits(min_=11)
    with pytest.raises(OutOfBoundError):
        value()


def test_max(value: ConfigValueInteger):
    assert value() is 10
    value.set_limits(max_=10)
    assert value() is 10
    value.set_limits(max_=9)
    with pytest.raises(OutOfBoundError):
        value()


def test_min_max(value: ConfigValueInteger):
    assert value() is 10
    value.set_limits(min_=10, max_=10)
    assert value() is 10
    value.set_limits(max_=9)
    with pytest.raises(OutOfBoundError):
        value()
    value.set_limits(min_=11, max_=11)
    with pytest.raises(OutOfBoundError):
        value()
