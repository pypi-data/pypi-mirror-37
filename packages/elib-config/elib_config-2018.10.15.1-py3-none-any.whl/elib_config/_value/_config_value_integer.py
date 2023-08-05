# coding=utf-8
"""
Config value that will be cast as a string
"""
# noinspection PyProtectedMember
from ._config_value import ConfigValue, SENTINEL
from ._exc import OutOfBoundError


class ConfigValueInteger(ConfigValue):
    """
    Config value that will be cast as a string
    """

    def __init__(self, *path: str, description: str, default=SENTINEL) -> None:
        super(ConfigValueInteger, self).__init__(*path, description=description, default=default)
        self._min = None
        self._max = None

    @property
    def type_name(self) -> str:
        """
        :return: user friendly type for this config value
        """
        return 'integer'

    def _raise_out_of_bound_error(self, value: int):
        raise OutOfBoundError(self.name, value, self._min, self._max)

    def _cast(self, raw_value) -> int:
        if not isinstance(raw_value, int) or isinstance(raw_value, bool):
            return self._raise_invalid_type_error()
        value = int(raw_value)
        if (self._min and value < self._min) or (self._max and value > self._max):
            return self._raise_out_of_bound_error(value)
        return value

    # pylint: disable=useless-super-delegation
    def __call__(self) -> int:
        return super(ConfigValueInteger, self).__call__()

    def set_limits(self, min_=None, max_=None):
        """
        Sets limits for this config value

        If the resulting integer is outside those limits, an exception will be raised

        :param min_: minima
        :param max_: maxima
        """
        self._min, self._max = min_, max_
