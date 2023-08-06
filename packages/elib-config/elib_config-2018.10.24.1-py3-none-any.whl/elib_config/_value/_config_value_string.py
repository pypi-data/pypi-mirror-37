# coding=utf-8
"""
Config value that will be cast as a string
"""
import tomlkit.container

from elib_config._types import Types
from ._config_value import ConfigValue


class ConfigValueString(ConfigValue):
    """
    Config value that will be cast as a string
    """

    @property
    def type_name(self) -> str:
        """
        :return: user friendly type for this config value
        """
        return Types.string

    def _cast(self, raw_value) -> str:
        if not isinstance(raw_value, str):
            self._raise_invalid_type_error()
        return raw_value

    # pylint: disable=useless-super-delegation
    def __call__(self) -> str:
        return super(ConfigValueString, self).__call__()

    def _toml_add_examples(self, toml_obj: tomlkit.container.Container):
        self._toml_comment(toml_obj, r'example = "some text inside double quotes"')
