# coding=utf-8
"""
Defines config values as instances of ConfigValue that can be called to obtain their values.

Values will be looked for in the OS environment first, then in the config file. If no value is found, the default will
be returned, or an exception will be raised.

Config value have strong type that will be checked and enforced at runtime.

They also have a description, which will be used to create the example config file.
"""
import abc
import typing

import tomlkit.container

SENTINEL: typing.Any = object()


class ConfigValueTOML(abc.ABC):
    """
    Abstract base class for config values that can be translated to TOML
    """
    description: str
    default: typing.Any  # noqa

    @property
    @abc.abstractmethod
    def key(self) -> str:
        """
        :return: last component of path
        :rtype: str
        """

    @property
    @abc.abstractmethod
    def friendly_type_name(self) -> str:
        """
        :return: friendly type name for the end-user
        :rtype: str
        """

    def _toml_add_description(self, toml_obj: tomlkit.container.Container):
        toml_obj.add(tomlkit.comment(self.description))

    def _toml_add_value_type(self, toml_obj: tomlkit.container.Container):
        toml_obj.add(tomlkit.comment(f'value type: {self.friendly_type_name}'))

    def _toml_add_comments(self, toml_obj: tomlkit.container.Container):
        self._toml_add_examples(toml_obj)
        if self.default != SENTINEL:
            comments = [
                'Setting this value is not required; you can leave it commented out.',
                'The default value (the one that will be used if you do not provide another) is shown below:',
            ]
            for comment in comments:
                toml_obj.add(tomlkit.comment(comment))
        else:
            toml_obj.add(tomlkit.comment('MANDATORY CONFIG VALUE: you *must* provide a value for this setting'))

    def _toml_add_value(self, toml_obj: tomlkit.container.Container, not_set: str):
        if self.default != SENTINEL:
            _doc = tomlkit.document()
            _doc[self.key] = self.default
            toml_obj.add(tomlkit.comment(_doc.as_string()))
        else:
            toml_obj[self.key] = not_set
            toml_obj.add(tomlkit.nl())

    @staticmethod
    def _toml_comment(toml_obj: tomlkit.container.Container, comment: str):
        toml_obj.add(tomlkit.comment(comment))

    @abc.abstractmethod
    def _toml_add_examples(self, toml_obj: tomlkit.container.Container):
        pass

    def add_to_toml_obj(self, toml_obj: tomlkit.container.Container, not_set: str):
        """
        Updates the given container in-place with this ConfigValue

        :param toml_obj: container to update
        :type toml_obj: tomlkit.container.Containers
        :param not_set: random UUID used to denote a value that has no default
        :type not_set: str
        """
        self._toml_add_description(toml_obj)
        self._toml_add_value_type(toml_obj)
        self._toml_add_comments(toml_obj)
        toml_obj.add(tomlkit.comment(''))
        self._toml_add_value(toml_obj, not_set)
