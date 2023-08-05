# coding=utf-8
"""
Reads and writes ESST's config to/from a file.
"""
import typing
import multiprocessing
from pathlib import Path

import toml

# noinspection PyProtectedMember
from elib_config._setup import ELIBConfig
# noinspection PyProtectedMember
from ._exc import ConfigFileNotFoundError, EmptyValueError, InvalidConfigFileError

CONFIG_LOCK = multiprocessing.Lock()
""":py:class:`multiprocessing.Lock` that blocks concurrent access to the config file by multiple processes"""


def _ensure_config_file_exists():
    """
    Makes sure the config file exists.

    :raises: :class:`epab.core.new_config.exc.ConfigFileNotFoundError`
    """
    config_file = Path(ELIBConfig.config_file_path).absolute()
    if not config_file.exists():
        raise ConfigFileNotFoundError(ELIBConfig.config_file_path)


def _read_file() -> typing.MutableMapping[str, typing.Any]:
    config_file = Path(ELIBConfig.config_file_path).absolute()
    if not config_file.exists():
        return {}
    with config_file.open(encoding='utf8') as stream:
        try:
            return toml.load(stream)
        except toml.TomlDecodeError as error:
            if error.args and 'Empty value is invalid' in error.args[0]:
                raise EmptyValueError(str(config_file))
            else:
                raise InvalidConfigFileError(str(config_file), error.args)


def _write_file(config: dict):
    config_file = Path(ELIBConfig.config_file_path).absolute()
    with config_file.open(mode='w', encoding='utf8') as stream:
        toml.dump(config, stream)


def read_config_file() -> typing.MutableMapping[str, typing.Any]:
    """
    Reads configuration from the disk.

    :return: configuration dictionary.
    :raises MissingConfigPackageError: raised if ``package`` is not ``None`` and it doesn't exist at the top level of
        the config file.
    """
    return _read_file()
