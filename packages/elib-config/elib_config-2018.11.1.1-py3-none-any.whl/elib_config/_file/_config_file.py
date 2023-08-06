# coding=utf-8
"""
Reads and writes ESST's config to/from a file.
"""
import typing
import multiprocessing
from pathlib import Path

import tomlkit
import tomlkit.exceptions

# noinspection PyProtectedMember
from elib_config._setup import ELIBConfig
# noinspection PyProtectedMember
from ._exc import ConfigFileNotFoundError, EmptyValueError

CONFIG_LOCK = multiprocessing.RLock()
""":py:class:`multiprocessing.RLock` that blocks concurrent access to the config file by multiple processes"""


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
            return tomlkit.parse(stream.read())
        except tomlkit.exceptions.UnexpectedCharError as err:
            if r"Unexpected character: '\n'" in err.args[0]:
                # noinspection PyProtectedMember
                raise EmptyValueError(str(config_file), err._line)  # pylint: disable=protected-access
            else:
                raise


def _write_file(config: dict):
    config_file = Path(ELIBConfig.config_file_path).absolute()
    with config_file.open(mode='w', encoding='utf8') as stream:
        stream.write(tomlkit.dumps(config))


def read_config_file() -> typing.MutableMapping[str, typing.Any]:
    """
    Reads configuration from the disk.

    :return: configuration dictionary.
    :raises MissingConfigPackageError: raised if ``package`` is not ``None`` and it doesn't exist at the top level of
        the config file.
    """
    return _read_file()
