# coding=utf-8
"""
Verifies that all configuration values have a valid setting
"""

from elib_config._setup import ELIBConfig
# noinspection PyProtectedMember
from elib_config._value._config_value import ConfigValue
# noinspection PyProtectedMember
from elib_config._value._exc import DuplicateConfigValueError


def validate_config():
    """
    Verifies that all configuration values have a valid setting
    """
    ELIBConfig.check()
    known_paths = set()
    for config_value in ConfigValue.config_values:
        if config_value.path not in known_paths:
            known_paths.add(config_value.path)
        else:
            raise DuplicateConfigValueError(config_value.path)
        config_value()
