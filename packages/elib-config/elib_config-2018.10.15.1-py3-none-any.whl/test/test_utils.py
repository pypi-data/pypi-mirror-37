# coding=utf-8

import pytest

# noinspection PyProtectedMember
from elib_config import _utils


@pytest.mark.parametrize(
    'raw_type,friendly_name',
    [
        (str, 'string'),
        (dict, 'dictionary'),
        (list, 'list'),
        (int, 'integer'),
        (float, 'float'),
        (bool, 'boolean'),
    ]
)
def test_friendly_type_name(raw_type, friendly_name):
    assert friendly_name == _utils.friendly_type_name(raw_type)


def test_unknown_type():
    with pytest.raises(ValueError, match='unknown type: .*'):
        # noinspection PyTypeChecker
        _utils.friendly_type_name(None)
