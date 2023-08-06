# coding=utf-8

import pytest

# noinspection PyProtectedMember
from elib_config import _utils


@pytest.mark.parametrize(
    'raw_type,friendly_name',
    [
        (str, 'string'),
        (dict, 'table'),
        (list, 'array'),
        (int, 'integer'),
        (float, 'float'),
        (bool, 'boolean'),
    ]
)
def test_friendly_type_name(raw_type, friendly_name):
    assert friendly_name == _utils.friendly_type_name(raw_type)
