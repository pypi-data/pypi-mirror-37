# coding=utf-8
"""
This module is responsible for writing an example config file in case it is missing or incorrect
"""
import typing
import uuid
from collections import defaultdict

import tomlkit
from tomlkit.container import Container as TOMLContainer

from elib_config._file._config_example_header import HEADER
# noinspection PyProtectedMember
from elib_config._setup import ELIBConfig
# noinspection PyProtectedMember
from elib_config._value._config_value import ConfigValue

_NOT_SET = uuid.uuid4().hex


def _nested_default_dict() -> defaultdict:
    return defaultdict(_nested_default_dict)


def _default_dict_to_dict(source) -> dict:
    for key, value in source.items():
        if isinstance(value, dict):
            source[key] = _default_dict_to_dict(value)
    return dict(source)


def _get_header() -> typing.List[str]:
    return HEADER.format(
        app_version=ELIBConfig.app_version,
        app_name=ELIBConfig.app_name,
        config_file_path=ELIBConfig.config_file_path,
        sep=ELIBConfig.config_sep_str,
    ).split('\n') + ['', 'START OF ACTUAL CONFIG FILE']


def _aggregate_config_values(config_values: typing.List[ConfigValue]) -> dict:
    """
    Returns a (sorted)

    :param config_values:
    :type config_values:
    :return:
    :rtype:
    """
    _keys: defaultdict = _nested_default_dict()
    _sorted_values = sorted(config_values, key=lambda x: x.name)
    for value in _sorted_values:
        value_keys = value.path.split(ELIBConfig.config_sep_str)
        this_config_key = _keys
        for sub_key in value_keys[:-1]:
            this_config_key = this_config_key[sub_key]
        this_config_key[value_keys[-1]] = value
    return _default_dict_to_dict(_keys)


def _add_config_values_to_toml_object(toml_obj: TOMLContainer, data: typing.Dict[str, typing.Union[dict, ConfigValue]]):
    for key_name, key_data in data.items():
        if isinstance(key_data, dict):
            table = tomlkit.table()
            _add_config_values_to_toml_object(table, key_data)
            toml_obj[key_name] = table
        else:
            key_data.add_to_toml_obj(toml_obj, _NOT_SET)


def write_example_config(example_file_path: str):
    """
    Writes an example config file using the config values declared so far

    :param example_file_path: path to write to
    """
    document = tomlkit.document()
    for header_line in _get_header():
        document.add(tomlkit.comment(header_line))
    config_keys = _aggregate_config_values(ConfigValue.config_values)
    _add_config_values_to_toml_object(document, config_keys)
    _doc_as_str = document.as_string().replace(f'"{_NOT_SET}"', '')
    with open(example_file_path, 'w') as stream:
        stream.write(_doc_as_str)
