# coding=utf-8
"""
Exceptions for the file package
"""

import typing

# noinspection PyProtectedMember
from elib_config._exc import ELIBConfigError


class _ConfigFileError(ELIBConfigError):
    """Base class for all exceptions related to the config file"""

    def __init__(self, config_file_path: str, msg: str) -> None:
        self.config_file_path = config_file_path
        self.msg = msg
        super(_ConfigFileError, self).__init__(
            f'{config_file_path}: {msg}'
        )


class IncompleteSetupError(ELIBConfigError):
    """Raised when elib_config is incomplete"""


class ConfigFileNotFoundError(_ConfigFileError):
    """Raised when the config file is missing"""

    def __init__(self, config_file_path: str) -> None:
        super(ConfigFileNotFoundError, self).__init__(
            config_file_path,
            'file not found'
        )


class InvalidConfigFileError(_ConfigFileError):
    """Raised when the format of the config file is invalid"""

    def __init__(self, config_file_path: str, additional_info: typing.Optional[typing.Iterable[str]] = None) -> None:
        if additional_info:
            _info = '\n' + ', '.join(additional_info)
        else:
            _info = ''
        super(InvalidConfigFileError, self).__init__(
            config_file_path,
            'config file could not be decoded; have a look at https://github.com/toml-lang/toml for the TOML '
            'language specification' + _info
        )


class EmptyValueError(_ConfigFileError):
    """Raised when a config value in the config file is empty"""

    def __init__(self, config_file_path: str) -> None:
        super(EmptyValueError, self).__init__(
            config_file_path,
            'there is an empty value in the configuration file; look for an equal sign ("=") with no value to its right'
        )
