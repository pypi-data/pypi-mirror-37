# coding=utf-8
"""
Config value that will be cast as a boolean
"""
import tomlkit.container

from elib_config._types import Types
from ._config_value import ConfigValue
from ._exc import ConfigValueTypeError


class ConfigValueBool(ConfigValue):
    """
    Config value that will be cast as a boolean
    """

    @property
    def type_name(self) -> str:
        """
        :return: user friendly type for this config value
        """
        return Types.boolean

    def _cast(self, raw_value) -> bool:
        if not isinstance(raw_value, bool):
            raise ConfigValueTypeError(
                self.path,
                f'invalid boolean expression: "{raw_value}"; use either "true" or "false" instead, without the quotes.'
            )

        return raw_value

    # pylint: disable=useless-super-delegation
    def __call__(self) -> bool:
        return super(ConfigValueBool, self).__call__()

    def _toml_add_examples(self, toml_obj: tomlkit.container.Container):
        self._toml_comment(toml_obj, '"true" and "false" are the only valid boolean values')
        self._toml_comment(toml_obj, 'example = true')
        self._toml_comment(toml_obj, 'example = false')
