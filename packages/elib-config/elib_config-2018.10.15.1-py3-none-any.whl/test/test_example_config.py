# coding=utf-8

import pathlib
import re

# noinspection PyProtectedMember
from elib_config._file import _config_example
# noinspection PyProtectedMember
from elib_config._value import _config_value
import elib_config


class DummyConfigValue(_config_value.ConfigValue):

    def _cast(self, raw_value):
        return raw_value

    @property
    def type_name(self) -> str:
        return 'test'


def _strip_header(file: str):
    file_path = pathlib.Path(file)
    content = pathlib.Path(file_path).read_text('utf8')
    new_content = re.sub(r'.*START OF ACTUAL CONFIG FILE', '', content, flags=re.MULTILINE)
    file_path.write_text(new_content, 'utf8')


def test_config_values_to_text():
    DummyConfigValue(
        'some', 'key',
        description='value1',
        default='test',
    )
    DummyConfigValue(
        'some', 'key2',
        description='value2',
        default='test',
    )
    _config_example.write_example_config('test')
    _, content = pathlib.Path('test').read_text('utf8').split('START OF ACTUAL CONFIG FILE\n\n\n')
    test_file = pathlib.Path('test.toml')
    test_file.write_text(content, 'utf8')
    import toml
    toml.loads(test_file.read_text('utf8'))
    assert content == """[some]
# value1
# value type: test
# This configuration is optional and comes with a default setting
# default: test
# key = 

# value2
# value type: test
# This configuration is optional and comes with a default setting
# default: test
# key2 = 
""", content


def test_config_values_to_text_mandatory_values():
    DummyConfigValue(
        'some', 'key',
        description='value1',
    )
    DummyConfigValue(
        'some', 'key2',
        description='value2',
        default='test',
    )
    elib_config.ConfigValueBool(
        'test_bool',
        description='value bool',
        default=True
    )
    _config_example.write_example_config('test')
    _, content = pathlib.Path('test').read_text('utf8').split('START OF ACTUAL CONFIG FILE\n\n\n')
    test_file = pathlib.Path('test.toml')
    test_file.write_text(content, 'utf8')
    import toml
    try:
        toml.loads(test_file.read_text('utf8'))
    except toml.TomlDecodeError as error:
        if 'Empty value is invalid' in error.args[0]:
            pass
        else:
            raise

    assert """# value bool
# value type: boolean
# This configuration is optional and comes with a default setting
# default: true
# test_bool = 


[some]
# value1
# value type: test
# MANDATORY CONFIG VALUE
key = 

# value2
# value type: test
# This configuration is optional and comes with a default setting
# default: test
# key2 = 
""" == content, content
