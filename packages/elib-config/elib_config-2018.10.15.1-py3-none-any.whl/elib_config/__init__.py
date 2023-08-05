# coding=utf-8
"""
This package manages configuration for other packages.

It is intended for my personal use only
"""

from pkg_resources import DistributionNotFound, get_distribution

# noinspection PyProtectedMember
from elib_config._file._exc import (
    ConfigFileNotFoundError, EmptyValueError, IncompleteSetupError, InvalidConfigFileError,
)
# noinspection PyProtectedMember
from elib_config._value._exc import (
    ConfigMissingValueError, ConfigTypeError, ConfigValueError, DuplicateConfigValueError, NotAFileError,
    NotAFolderError, OutOfBoundError, PathMustExistError,
)
# noinspection PyProtectedMember
from ._file._config_example import write_example_config
from ._setup import ELIBConfig
# noinspection PyProtectedMember
from ._value._config_value import SENTINEL, validate_config
# noinspection PyProtectedMember
from ._value._config_value_bool import ConfigValueBool
# noinspection PyProtectedMember
from ._value._config_value_integer import ConfigValueInteger
# noinspection PyProtectedMember
from ._value._config_value_list import ConfigValueList
# noinspection PyProtectedMember
from ._value._config_value_path import ConfigValuePath
# noinspection PyProtectedMember
from ._value._config_value_string import ConfigValueString

try:
    __version__ = get_distribution('elib_config').version
except DistributionNotFound:  # pragma: no cover
    # package is not installed
    __version__ = 'not installed'
