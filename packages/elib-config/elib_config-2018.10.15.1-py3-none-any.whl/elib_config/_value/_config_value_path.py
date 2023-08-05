# coding=utf-8
"""
Config value that will be cast as a `pathlib.Path`

Provides a few helpers to further customize the behaviour for path config values
"""
import typing
from pathlib import Path

# noinspection PyProtectedMember
from ._config_value import ConfigValue, SENTINEL
# noinspection PyProtectedMember
from ._exc import NotAFileError, NotAFolderError, PathMustExistError


class ConfigValuePath(ConfigValue):
    """
    Config value that will be cast as a `pathlib.Path`
    """

    def __init__(self, *path: str, description: str, default: typing.Any = SENTINEL) -> None:  # type: ignore
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
        self._must_be_file = True

    def must_be_dir(self):
        """
        Indicates that, if it exists, this path must be a directory
        """
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
        return 'path'

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
