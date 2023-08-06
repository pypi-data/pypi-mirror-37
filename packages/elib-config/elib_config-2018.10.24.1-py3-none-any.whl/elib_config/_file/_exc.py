# coding=utf-8
"""
Exceptions for the file package
"""

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


class EmptyValueError(_ConfigFileError):
    """Raised when a config value in the config file is empty"""

    def __init__(self, config_file_path: str, line_no: int) -> None:
        super(EmptyValueError, self).__init__(
            config_file_path,
            'empty value found at line: ' + str(line_no)
        )
