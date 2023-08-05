# coding=utf-8

import os
import sys
from pathlib import Path

import pytest
from mockito import unstub

_HERE = Path('.').absolute()


def pytest_configure(config):
    """
    Runs at tests startup

    Args:
        config: pytest config args
    """
    print('Pytest config:', config.option)
    setattr(sys, '_called_from_test', True)


# noinspection SpellCheckingInspection
def pytest_unconfigure(config):
    """Tear down"""
    assert config
    delattr(sys, '_called_from_test')


def pytest_addoption(parser):
    parser.addoption("--long", action="store_true",
                     help="run long tests")


def pytest_runtest_setup(item):
    long_marker = item.get_marker("long")
    if long_marker is not None and not item.config.getoption('long'):
        pytest.skip(f'{item.location}: skipping long tests')


@pytest.fixture(autouse=True)
def clean_os_env():
    env = os.environ.copy()
    yield
    for key, value in env.items():
        os.environ[key] = value
    for key in os.environ.keys():
        if key not in env.keys():
            del os.environ[key]


@pytest.fixture(autouse=True)
def _global_tear_down(tmpdir, monkeypatch):
    """
    Maintains a sane environment between tests
    """
    try:
        monkeypatch.delenv('APPVEYOR')
    except KeyError:
        pass
    current_dir = os.getcwd()
    folder = Path(tmpdir).absolute()
    os.chdir(folder)
    yield
    unstub()
    # noinspection PyProtectedMember
    from elib_config._setup import ELIBConfig
    ELIBConfig.setup(
        app_version='not_set',
        app_name='not_set',
        config_file_path='not_set',
        config_sep_str='not_set'
    )
    os.chdir(current_dir)


@pytest.fixture(autouse=True)
def dummy_setup(request):
    """
    Simple fixture to setup dummy values for the package config
    """
    marker = request.node.get_marker('skip_setup')
    if marker is not None:
        return

    # noinspection PyProtectedMember
    from elib_config._setup import ELIBConfig
    ELIBConfig.setup(
        app_version='0.1',
        app_name='test',
        config_file_path='config.toml',
        config_sep_str='__',
    )


@pytest.fixture(autouse=True)
def _clean_known_values():
    # noinspection PyProtectedMember
    from elib_config._value import _config_value
    _config_value.ConfigValue.config_values = []
