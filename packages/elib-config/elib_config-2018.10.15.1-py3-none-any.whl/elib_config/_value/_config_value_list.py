# coding=utf-8
"""
Config value that will be cast as a list
"""

import typing

# noinspection PyProtectedMember
from elib_config._utils import friendly_type_name
# noinspection PyProtectedMember
from ._config_value import ConfigValue, SENTINEL
# noinspection PyProtectedMember
from ._exc import ConfigTypeError


class ConfigValueList(ConfigValue):
    """
    Config value that will be cast as a list

    Additionally, all element of the list will be type-checked
    """

    @property
    def type_name(self) -> str:
        """
        :return: user friendly type for this config value
        """
        return f'List of {self._expected_element_type}s'

    def __init__(self, *path: str, element_type: typing.Type, description: str, default: typing.Any = SENTINEL) -> None:
        self.element_type = element_type
        super(ConfigValueList, self).__init__(*path, description=description, default=default)

    @property
    def _expected_element_type(self) -> str:
        return friendly_type_name(self.element_type)

    def _cast(self, raw_value: object) -> list:
        if not isinstance(raw_value, list):
            return self._raise_invalid_type_error()
        for index, item in enumerate(raw_value):
            if not isinstance(item, self.element_type):
                actual_type = friendly_type_name(type(item))
                raise ConfigTypeError(
                    self.path,
                    f'{self.name}: item at index {index} should be a "{self._expected_element_type}", but is '
                    f'"{actual_type}" instead'
                )
        return raw_value

    # pylint: disable=useless-super-delegation
    def __call__(self) -> list:
        return super(ConfigValueList, self).__call__()
