# coding=utf-8
"""
Config value that will be cast as a list
"""

import typing

import tomlkit.container

from elib_config._utils import friendly_type_name
from ._config_value import ConfigValue, SENTINEL
from ._exc import ConfigValueTypeError
from elib_config._types import Types


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
        return Types.array

    @property
    def friendly_type_name(self) -> str:
        """
        :return: user friendly type for this config value
        """
        return f'{Types.array} of {self._expected_element_type}s'

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
                raise ConfigValueTypeError(
                    self.path,
                    f'{self.name}: item at index {index} should be a "{self._expected_element_type}", but is '
                    f'"{actual_type}" instead'
                )
        return raw_value

    # pylint: disable=useless-super-delegation
    def __call__(self) -> list:
        return super(ConfigValueList, self).__call__()

    def _toml_add_value_type(self, toml_obj: tomlkit.container.Container):
        super(ConfigValueList, self)._toml_add_value_type(toml_obj)
        self._toml_comment(toml_obj, f'Array elements must be type: {self._expected_element_type}')

    def _toml_add_examples(self, toml_obj: tomlkit.container.Container):
        if self.element_type == str:
            self._toml_comment(toml_obj, 'example = ["a", "b", "c", "d e"] # A list of strings')
        elif self.element_type == int:
            self._toml_comment(toml_obj, 'example = [1, 2, 3, 4, 5] # A list of integers')
        elif self.element_type == float:
            self._toml_comment(toml_obj, 'example = [1.0, 2.0, 3.0] # A list of floats')
        else:
            raise KeyError(f'unmanaged element type: {self.element_type}')
