# coding=utf-8

import pathlib

import pytest

from elib_config import (
    ConfigMissingValueError, ConfigValueBool, ConfigValueInteger, ConfigValueList, ConfigValuePath, ConfigValueString,
    DuplicateConfigValueError, validate_config,
)


def _create_values_with_default():
    ConfigValueBool('bool', description='dummy', default=True)
    ConfigValueString('string', description='dummy', default='string')
    ConfigValueInteger('integer', description='dummy', default=10)
    ConfigValuePath('path', description='dummy', default=pathlib.Path('.'))
    ConfigValueList('list', description='dummy', default=[], element_type=str)


def test_valid_bare_config():
    _create_values_with_default()
    validate_config()


@pytest.mark.parametrize(
    'val_cls',
    [ConfigValueBool, ConfigValueString, ConfigValueInteger, ConfigValuePath]
)
def test_config_without_default(val_cls):
    val_cls('val_name', description='dummy')
    with pytest.raises(ConfigMissingValueError):
        validate_config()


@pytest.mark.parametrize(
    'val_name',
    ('bool', 'string', 'integer', 'path', 'list')
)
def test_duplicate_path(val_name):
    _create_values_with_default()
    with pytest.raises(DuplicateConfigValueError):
        ConfigValueBool(val_name, description='dummy', default=True)
        validate_config()
