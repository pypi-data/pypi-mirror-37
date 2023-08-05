# coding=utf-8
"""
Utils for elib_config
"""
import typing


def friendly_type_name(raw_type: typing.Type) -> str:
    """
    Returns a user-friendly type name

    :param raw_type: raw type (str, int, ...)
    :return: user friendly type as string
    """
    if raw_type is str:
        return 'string'
    try:
        if issubclass(raw_type, dict):
            return 'dictionary'
    except TypeError:
        pass
    if raw_type is int:
        return 'integer'
    if raw_type is float:
        return 'float'
    if raw_type is bool:
        return 'boolean'
    if raw_type is list:
        return 'list'

    raise ValueError(f'unknown type: {raw_type}')
