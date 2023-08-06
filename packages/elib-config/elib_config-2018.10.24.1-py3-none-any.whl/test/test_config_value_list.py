# coding=utf-8

import pathlib

import pytest

# noinspection PyProtectedMember
from elib_config import ConfigMissingValueError, ConfigValueTypeError, ConfigValueList, _utils, _types


@pytest.fixture(name='value')
def _dummy_string_value():
    yield ConfigValueList(
        'key',
        element_type=str,
        description='desc',
        default=['some', 'list'],
    )


def test_no_default():
    value = ConfigValueList(
        'test', 'value',
        element_type=str,
        description='test',
    )
    with pytest.raises(ConfigMissingValueError):
        value()


def test_string_value_default(value: ConfigValueList):
    assert value() == ['some', 'list']


def test_string_value_type_name(value: ConfigValueList):
    assert value.type_name == 'array'
    assert value.friendly_type_name == 'array of strings'


@pytest.mark.parametrize(
    'file_value,wrong_type',
    [
        (10, "integer"),
        (10.01, "float"),
        ('"some string"', 'string'),
        ('true', 'boolean'),
        ('{some = "dict"}', 'table'),
    ]
)
def test_invalid_cast_type_from_config_file(value: ConfigValueList, file_value, wrong_type):
    pathlib.Path('config.toml').write_text(f'key = {file_value}')
    exc_msg = f'{value.name}: config value must be of type "{_types.Types.array}", got "{wrong_type}" instead'
    with pytest.raises(ConfigValueTypeError, match=exc_msg):
        value()


def test_valid_cast_type_from_config_file(value: ConfigValueList):
    pathlib.Path('config.toml').write_text(f'key = ["some", "other", "list"]')
    assert value() == ['some', 'other', 'list']


@pytest.mark.parametrize(
    'not_a_string',
    (True, False, 10, 10.05, ['another', 'list'], {'a': 'dict'})
)
def test_element_type_check(value: ConfigValueList, not_a_string):
    value.default = ['string', 'string_too', not_a_string]
    actual_type = _utils.friendly_type_name(type(not_a_string))
    error = f'{value.name}: item at index 2 should be a "string", but is "{actual_type}" instead'
    with pytest.raises(ConfigValueTypeError, match=error):
        value()


@pytest.mark.parametrize(
    'not_a_string',
    ('true', 'false', '10', '10.05', '["another", "list"]', '{a = "dict"}')
)
def test_element_type_check_from_file(value: ConfigValueList, not_a_string):
    pathlib.Path('config.toml').write_text(f'key = [ {not_a_string} ]')
    error = f'{value.name}: item at index 0 should be a "string", but is .* instead'
    with pytest.raises(ConfigValueTypeError, match=error):
        value()


def test_toml_example_unmanaged_element_type():
    value = ConfigValueList('test', element_type=bool, description='')
    with pytest.raises(KeyError):
        value._toml_add_examples({})
