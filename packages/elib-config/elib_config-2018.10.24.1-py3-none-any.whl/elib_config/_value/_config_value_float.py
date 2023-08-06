# coding=utf-8
"""
Config value that will be cast as a string
"""
import typing
import tomlkit.container

from ._config_value_integer import ConfigValueInteger
from elib_config._types import Types


class ConfigValueFloat(ConfigValueInteger):
    """
    Config value that will be cast as a string
    """

    @property
    def type_name(self) -> str:
        """
        :return: user friendly type for this config value
        """
        return Types.float

    def _cast(self, raw_value) -> float:
        if not isinstance(raw_value, float):
            return self._raise_invalid_type_error()
        value = float(raw_value)
        if (self._min and value < self._min) or (self._max and value > self._max):
            return self._raise_out_of_bound_error(value)
        return value

    # pylint: disable=useless-super-delegation
    def __call__(self) -> float:  # mypy: ignore
        return super(ConfigValueFloat, self).__call__()

    def set_limits(self, min_: typing.Optional[float] = None, max_: typing.Optional[float] = None):
        """
        Sets limits for this config value

        If the resulting integer is outside those limits, an exception will be raised

        :param min_: minima
        :param max_: maxima
        """
        self._min, self._max = min_, max_

    def _toml_add_examples(self, toml_obj: tomlkit.container.Container):
        self._toml_comment(toml_obj, 'example = 132.5')
        self._toml_comment(toml_obj, 'example = 0.0')
        self._toml_comment(toml_obj, 'example = -20.765')
