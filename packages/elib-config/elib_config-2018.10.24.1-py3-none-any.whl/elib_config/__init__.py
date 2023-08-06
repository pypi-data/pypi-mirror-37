# coding=utf-8
"""
This package manages configuration for other packages.

It is intended for my personal use only
"""

from pkg_resources import DistributionNotFound, get_distribution

# noinspection PyProtectedMember
from elib_config._file._exc import (
    ConfigFileNotFoundError, EmptyValueError, IncompleteSetupError,
)
# noinspection PyProtectedMember
from elib_config._types import Types
# noinspection PyProtectedMember
from elib_config._value._exc import (
    ConfigMissingValueError, ConfigValueError, ConfigValueTypeError, DuplicateConfigValueError, MissingTableKeyError,
    NotAFileError, NotAFolderError, OutOfBoundError, PathMustExistError, TableKeyTypeError,
)
# noinspection PyProtectedMember
from ._file._config_example import write_example_config
# noinspection PyProtectedMember
from ._logging import LOGGER
from ._setup import ELIBConfig
from ._validate import validate_config
# noinspection PyProtectedMember
from ._value._config_value import SENTINEL
# noinspection PyProtectedMember
from ._value._config_value_bool import ConfigValueBool
# noinspection PyProtectedMember
from ._value._config_value_float import ConfigValueFloat
# noinspection PyProtectedMember
from ._value._config_value_integer import ConfigValueInteger
# noinspection PyProtectedMember
from ._value._config_value_list import ConfigValueList
# noinspection PyProtectedMember
from ._value._config_value_path import ConfigValuePath
# noinspection PyProtectedMember
from ._value._config_value_string import ConfigValueString
# noinspection PyProtectedMember
from ._value._config_value_table import ConfigValueTableArray, ConfigValueTableKey

try:
    __version__ = get_distribution('elib_config').version
except DistributionNotFound:  # pragma: no cover
    # package is not installed
    __version__ = 'not installed'
