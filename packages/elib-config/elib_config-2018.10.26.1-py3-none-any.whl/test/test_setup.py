# coding=utf-8
"""
Tests for `elib_config._setup.py`
"""

import pytest

# noinspection PyProtectedMember
import elib_config._file._exc
# noinspection PyProtectedMember
from elib_config import _setup


@pytest.mark.skip_setup
def test_no_setup():
    with pytest.raises(elib_config._file._exc.IncompleteSetupError):
        _setup.ELIBConfig.check()


def test_correct_setup():
    _setup.ELIBConfig.check()


@pytest.mark.parametrize(
    'attrib',
    ['app_version', 'app_name', 'config_file_path', 'config_sep_str']
)
def test_partial_setup(attrib):
    setattr(_setup.ELIBConfig, attrib, 'not_set')
    with pytest.raises(elib_config._file._exc.IncompleteSetupError):
        _setup.ELIBConfig.check()
