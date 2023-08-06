# coding=utf-8
"""
Utils for elib_config
"""
import typing

import tomlkit.container
import tomlkit.items

from elib_config._logging import LOGGER
from elib_config._types import Types

_TRANSLATE_TYPE = {
    bool: Types.boolean,
    str: Types.string,
    tomlkit.items.String: Types.string,
    int: Types.integer,
    tomlkit.items.Integer: Types.integer,
    float: Types.float,
    tomlkit.items.Float: Types.float,
    list: Types.array,
    dict: Types.table,
    tomlkit.container.Container: Types.table,

}


def friendly_type_name(raw_type: typing.Type) -> str:
    """
    Returns a user-friendly type name

    :param raw_type: raw type (str, int, ...)
    :return: user friendly type as string
    """
    try:
        return _TRANSLATE_TYPE[raw_type]
    except KeyError:
        LOGGER.error('unmanaged value type: %s', raw_type)
        return str(raw_type)
