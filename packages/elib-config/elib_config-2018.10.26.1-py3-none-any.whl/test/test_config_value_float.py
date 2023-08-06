# coding=utf-8

import pathlib

import pytest

from elib_config import ConfigMissingValueError, ConfigValueTypeError, ConfigValueFloat, OutOfBoundError


@pytest.fixture(name='value')
def _dummy_string_value():
    yield ConfigValueFloat(
        'key',
        description='desc',
        default=10.0,
    )


def test_no_default():
    value = ConfigValueFloat(
        'test', 'value',
        description='test',
    )
    with pytest.raises(ConfigMissingValueError):
        value()


def test_string_value_default(value):
    assert value() == 10.0


def test_string_value_type_name(value):
    assert value.type_name == 'float'


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
    exc_msg = f'{value.name}: config value must be of type "float", got .* instead'
    with pytest.raises(ConfigValueTypeError, match=exc_msg):
        value()


def test_valid_cast_type_from_config_file(value):
    pathlib.Path('config.toml').write_text(f'key = 5.0')
    assert value() == 5.0


def test_min(value: ConfigValueFloat):
    assert value() == 10.0
    value.set_limits(min_=10.0)
    assert value() == 10.0
    value.set_limits(min_=11.0)
    with pytest.raises(OutOfBoundError):
        value()


def test_max(value: ConfigValueFloat):
    assert value() == 10.0
    value.set_limits(max_=10.0)
    assert value() == 10.0
    value.set_limits(max_=9.0)
    with pytest.raises(OutOfBoundError):
        value()


def test_min_max(value: ConfigValueFloat):
    assert value() == 10.0
    value.set_limits(min_=10.0, max_=10.0)
    assert value() == 10.0
    value.set_limits(max_=9.0)
    with pytest.raises(OutOfBoundError):
        value()
    value.set_limits(min_=11.0, max_=11.0)
    with pytest.raises(OutOfBoundError):
        value()
