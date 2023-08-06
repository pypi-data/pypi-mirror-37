# coding=utf-8


# noinspection PyProtectedMember
from elib_config import _setup
# noinspection PyProtectedMember
from elib_config._value import _config_value


class DummyValue(_config_value.ConfigValue):

    def _cast(self, raw_value):
        return raw_value

    @property
    def type_name(self) -> str:
        return 'dummy'

    def _toml_add_examples(self):
        pass


def test_config_value_with_root_path():
    value = DummyValue(
        'key',
        description='dummy',
        default='test'
    )
    assert value.path == 'key'
    _setup.ELIBConfig.root_path = ['MyApp']
    value = DummyValue(
        'key',
        description='dummy',
        default='test'
    )
    assert value.path == 'MyApp__key'
    _setup.ELIBConfig.root_path = ['my', 'awesome', 'app']
    value = DummyValue(
        'key',
        description='dummy',
        default='test'
    )
    assert value.path == 'my__awesome__app__key'
