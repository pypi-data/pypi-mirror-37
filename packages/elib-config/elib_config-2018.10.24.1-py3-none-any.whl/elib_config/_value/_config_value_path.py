# coding=utf-8
"""
Config value that will be cast as a `pathlib.Path`

Provides a few helpers to further customize the behaviour for path config values
"""
import typing
from pathlib import Path

import tomlkit.container

from ._config_value import ConfigValue, SENTINEL
from ._exc import NotAFileError, NotAFolderError, PathMustExistError
from elib_config._types import Types


class ConfigValuePath(ConfigValue):
    """
    Config value that will be cast as a `pathlib.Path`
    """

    def __init__(self,
                 *path: str,
                 description: str,
                 default: typing.Any = SENTINEL,
                 ) -> None:
        ConfigValue.__init__(self, *path, description=description, default=default)
        self._must_be_file: bool = False
        self._must_be_dir: bool = False
        self._create_dir: bool = False
        self._must_exist: bool = False

    def must_exist(self):
        """
        Indicates this path must exist before runtime
        """
        self._must_exist = True

    def must_be_file(self):
        """
        Indicates that, if it exists, this path must be a file
        """
        if self._must_be_dir:
            raise AttributeError('path config value cannot be both a file and a directory')
        self._must_be_file = True

    def must_be_dir(self):
        """
        Indicates that, if it exists, this path must be a directory
        """
        if self._must_be_file:
            raise AttributeError('path config value cannot be both a file and a directory')
        self._must_be_dir = True

    def create_dir(self):
        """
        Indicates that, if it doesn't exist already, this path will be created as a directory
        """
        self._create_dir = True

    @property
    def type_name(self) -> str:
        """
        :return: user friendly type for this config value
        """
        return Types.path

    @property
    def friendly_type_name(self) -> str:
        """
        :return: friendly type name for the end-user
        :rtype: str
        """
        _constraints_set = []
        if self._must_be_dir:
            _constraints_set.append('must be a directory')
        if self._must_be_file:
            _constraints_set.append('must be a file')
        if self._must_exist:
            _constraints_set.append('must already exist')
        _constraints_as_str = ' (' + ', '.join(_constraints_set) + ')' if _constraints_set else ''
        return 'path' + _constraints_as_str

    def _cast(self, raw_value) -> Path:
        try:
            path = Path(raw_value)
        except TypeError:
            return self._raise_invalid_type_error()
        else:
            if self._must_exist and not path.exists():
                raise PathMustExistError(self.path)
            if path.exists() and self._must_be_dir and not path.is_dir():
                raise NotAFolderError(self.path)
            if path.exists() and self._must_be_file and not path.is_file():
                raise NotAFileError(self.path)
            if not path.exists() and self._create_dir:
                path.mkdir(parents=True)
            return path.absolute()

    # pylint: disable=useless-super-delegation
    def __call__(self) -> Path:
        return super(ConfigValuePath, self).__call__()

    def _toml_add_examples(self, toml_obj: tomlkit.container.Container):
        self._toml_comment(toml_obj, r'WARNING: backslash characters ("\") must be doubled.')
        self._toml_comment(toml_obj, 'Alternatively, you can use the forward slash: "/" (even on Windows).')
        self._toml_comment(toml_obj, r'example = c:\\some\\folder')
        self._toml_comment(toml_obj, r'example = c:\\some\\folder\\file.ext')
        self._toml_comment(toml_obj, r'example = c:/this/is/valid/too')
