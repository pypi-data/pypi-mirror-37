# coding=utf-8

import pathlib

import pytest
import tomlkit.exceptions

from elib_config import ConfigFileNotFoundError, EmptyValueError
# noinspection PyProtectedMember
from elib_config._file import _config_file


def test_ensure_config_file_exists_missing():
    with pytest.raises(ConfigFileNotFoundError):
        _config_file._ensure_config_file_exists()


def test_ensure_config_file_exists():
    pathlib.Path('config.toml').touch()
    _config_file._ensure_config_file_exists()


def test_read_file_empty():
    config = _config_file._read_file()
    assert isinstance(config, dict)
    assert not config


def test_read_file_basic():
    pathlib.Path('config.toml').write_text('key = "value"')
    config = _config_file._read_file()
    assert isinstance(config, dict)
    assert config
    assert 'key' in config
    assert config['key'] == 'value'


@pytest.mark.parametrize(
    'file_content',
    [
        'key: value',
        'key = value',
    ]
)
def test_invalid_file(file_content):
    pathlib.Path('config.toml').write_text(file_content)
    with pytest.raises(tomlkit.exceptions.UnexpectedCharError):
        _config_file._read_file()


def test_empty_value():
    pathlib.Path('config.toml').write_text("""[some]
    key = 
    """)
    with pytest.raises(EmptyValueError):
        _config_file.read_config_file()


def test_write_file():
    config_file_path = pathlib.Path('config.toml')
    original_config = _config_file.read_config_file()
    assert original_config == {}
    assert not config_file_path.exists()
    new_config = {'key': 'value'}
    _config_file._write_file(new_config)
    assert config_file_path.exists()
    assert _config_file.read_config_file() == new_config
