# coding=utf-8
"""
This module is responsible for writing an example config file in case it is missing or incorrect
"""
import textwrap
import typing

import toml

# noinspection PyProtectedMember
from elib_config._setup import ELIBConfig
# noinspection PyProtectedMember
from elib_config._value._config_value import ConfigValue, SENTINEL
# noinspection PyProtectedMember
from ._config_example_header import HEADER


def _get_header() -> str:
    header = HEADER.format(
        app_version=ELIBConfig.app_version,
        app_name=ELIBConfig.app_name,
        config_file_path=ELIBConfig.config_file_path,
        sep=ELIBConfig.config_sep_str,
    )
    return '# ' + str('\n# '.join(header.split('\n')).rstrip()) + '\n#\n# START OF ACTUAL CONFIG FILE\n\n'


def _aggregate_config_values(config_values: list) -> dict:
    config_keys: dict = {}
    for value in config_values:
        value_keys = value.path.split(ELIBConfig.config_sep_str)
        this_config_key = config_keys
        for key in value_keys[:-1]:
            if key not in this_config_key:
                this_config_key[key] = {}
            this_config_key = this_config_key[key]
        this_config_key[value_keys[-1]] = value
    return config_keys


def _extract_info(config_keys: dict) -> dict:
    for key in config_keys:
        if isinstance(config_keys[key], dict):
            config_keys[key] = _extract_info(config_keys[key])
        else:
            value: ConfigValue = config_keys[key]
            if value.default is SENTINEL:
                _default: typing.Any = 'SENTINEL'
            else:
                if value.type_name == 'boolean':
                    _default = str(value.default).lower()
                else:
                    _default = value.default
            config_keys[key] = f'{value.description}||{value.type_name}||{_default}'
    return config_keys


def _add_comments(config_text: str) -> str:
    result = []
    for line in config_text.splitlines():
        if ' = ' in line:
            line = line.replace('"', '')
            key_name, meta = line.split(' = ')
            description, type_name, default = meta.split('||')
            description = '\n'.join(
                textwrap.wrap(
                    description,
                    width=120,
                    initial_indent='# ',
                    subsequent_indent='# ',
                    break_long_words=False,
                )
            )
            result.append(description)
            result.append(f'# value type: {type_name}')
            if default == 'SENTINEL':
                result.append('# MANDATORY CONFIG VALUE')
                result.append(f'{key_name} = ')
            else:
                result.append('# This configuration is optional and comes with a default setting')
                result.append(f'# default: {default}')
                result.append(f'# {key_name} = ')
            result.append('')
        else:
            result.append(line)
    return '\n'.join(result)


def write_example_config(example_file_path: str):
    """
    Writes an example config file using the config values declared so far

    :param example_file_path: path to write to
    """
    config_keys = _aggregate_config_values(ConfigValue.config_values)
    config_meta = _extract_info(config_keys)
    config_text = toml.dumps(config_meta)
    commented_text = _add_comments(config_text)
    header_text = _get_header()
    final_text = '\n'.join((header_text, commented_text))
    with open(example_file_path, 'w') as stream:
        stream.write(final_text)
