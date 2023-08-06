# coding=utf-8

import pathlib
import re

import pytest
import dataclasses
import typing

import tomlkit
# noinspection PyProtectedMember
from elib_config._file import _config_example
# noinspection PyProtectedMember
from elib_config._value._config_value import ConfigValue
import elib_config


def _strip_header(file: str):
    file_path = pathlib.Path(file)
    content = pathlib.Path(file_path).read_text('utf8')
    new_content = re.sub(r'.*START OF ACTUAL CONFIG FILE', '', content, flags=re.MULTILINE)
    file_path.write_text(new_content, 'utf8')


@dataclasses.dataclass
class TestCase:
    value_cls: typing.Type[ConfigValue]
    path: typing.Iterable[str]
    run_after: typing.List = dataclasses.field(default_factory=list)
    default: typing.Optional[typing.Any] = None
    list_elements_type: typing.Optional[typing.Type] = None
    keys: typing.Optional[typing.Iterable[elib_config.ConfigValueTableKey]] = None

    def create(self):
        kwargs = {
            'description': 'desc',
        }
        if self.default is not None:
            kwargs['default'] = self.default
        if self.list_elements_type is not None:
            kwargs['element_type'] = self.list_elements_type
        if self.keys is not None:
            kwargs['keys'] = self.keys
        obj = self.value_cls(*self.path, **kwargs)
        for _func_name in self.run_after:
            getattr(obj, _func_name)()


TEST_DATA = [
    (
        TestCase(value_cls=elib_config.ConfigValueBool, path=('some', 'value'), default=True),
        """[some]
# desc
# value type: boolean
# "true" and "false" are the only valid boolean values
# example = true
# example = false
# Setting this value is not required; you can leave it commented out.
# The default value (the one that will be used if you do not provide another) is shown below:
# 
# value = true

"""
    ),
    (
        TestCase(value_cls=elib_config.ConfigValueBool, path=('some', 'value')),
        """[some]
# desc
# value type: boolean
# "true" and "false" are the only valid boolean values
# example = true
# example = false
# MANDATORY CONFIG VALUE: you *must* provide a value for this setting
# 
value = 

"""
    ),
    (
        TestCase(value_cls=elib_config.ConfigValueBool, path=('some', 'deeply', 'nested', 'value')),
        """[some]
[some.deeply]
[some.deeply.nested]
# desc
# value type: boolean
# "true" and "false" are the only valid boolean values
# example = true
# example = false
# MANDATORY CONFIG VALUE: you *must* provide a value for this setting
# 
value = 

"""
    ),
    (
        TestCase(value_cls=elib_config.ConfigValueBool, path=('value',)),
        """# desc
# value type: boolean
# "true" and "false" are the only valid boolean values
# example = true
# example = false
# MANDATORY CONFIG VALUE: you *must* provide a value for this setting
# 
value = 

"""
    ),
    (
        TestCase(value_cls=elib_config.ConfigValueString, path=('value',)),
        """# desc
# value type: string
# example = "some text inside double quotes"
# MANDATORY CONFIG VALUE: you *must* provide a value for this setting
# 
value = 

"""
    ),
    (
        TestCase(value_cls=elib_config.ConfigValueInteger, path=('value',)),
        """# desc
# value type: integer
# example = 10
# example = 0
# example = -5
# MANDATORY CONFIG VALUE: you *must* provide a value for this setting
# 
value = 

"""
    ),
    (
        TestCase(value_cls=elib_config.ConfigValueFloat, path=('value',)),
        """# desc
# value type: float
# example = 132.5
# example = 0.0
# example = -20.765
# MANDATORY CONFIG VALUE: you *must* provide a value for this setting
# 
value = 

"""
    ),
    (
        TestCase(value_cls=elib_config.ConfigValueList, path=('value',), list_elements_type=str),
        """# desc
# value type: array of strings
# Array elements must be type: string
# example = ["a", "b", "c", "d e"] # A list of strings
# MANDATORY CONFIG VALUE: you *must* provide a value for this setting
# 
value = 

"""
    ),
    (
        TestCase(value_cls=elib_config.ConfigValueList, path=('value',), list_elements_type=float),
        """# desc
# value type: array of floats
# Array elements must be type: float
# example = [1.0, 2.0, 3.0] # A list of floats
# MANDATORY CONFIG VALUE: you *must* provide a value for this setting
# 
value = 

"""
    ),
    (
        TestCase(value_cls=elib_config.ConfigValueList, path=('value',), list_elements_type=int),
        """# desc
# value type: array of integers
# Array elements must be type: integer
# example = [1, 2, 3, 4, 5] # A list of integers
# MANDATORY CONFIG VALUE: you *must* provide a value for this setting
# 
value = 

"""
    ),
    (
        TestCase(value_cls=elib_config.ConfigValuePath, path=('value',)),
        r"""# desc
# value type: path
# WARNING: backslash characters ("\") must be doubled.
# Alternatively, you can use the forward slash: "/" (even on Windows).
# example = c:\\some\\folder
# example = c:\\some\\folder\\file.ext
# example = c:/this/is/valid/too
# MANDATORY CONFIG VALUE: you *must* provide a value for this setting
# 
value = 

"""
    ),
    (
        TestCase(value_cls=elib_config.ConfigValuePath, path=('value',), run_after=['must_be_file']),
        r"""# desc
# value type: path (must be a file)
# WARNING: backslash characters ("\") must be doubled.
# Alternatively, you can use the forward slash: "/" (even on Windows).
# example = c:\\some\\folder
# example = c:\\some\\folder\\file.ext
# example = c:/this/is/valid/too
# MANDATORY CONFIG VALUE: you *must* provide a value for this setting
# 
value = 

"""
    ),
    (
        TestCase(value_cls=elib_config.ConfigValuePath, path=('value',), run_after=['must_be_dir']),
        r"""# desc
# value type: path (must be a directory)
# WARNING: backslash characters ("\") must be doubled.
# Alternatively, you can use the forward slash: "/" (even on Windows).
# example = c:\\some\\folder
# example = c:\\some\\folder\\file.ext
# example = c:/this/is/valid/too
# MANDATORY CONFIG VALUE: you *must* provide a value for this setting
# 
value = 

"""
    ),
    (
        TestCase(value_cls=elib_config.ConfigValuePath, path=('value',), run_after=['must_exist']),
        r"""# desc
# value type: path (must already exist)
# WARNING: backslash characters ("\") must be doubled.
# Alternatively, you can use the forward slash: "/" (even on Windows).
# example = c:\\some\\folder
# example = c:\\some\\folder\\file.ext
# example = c:/this/is/valid/too
# MANDATORY CONFIG VALUE: you *must* provide a value for this setting
# 
value = 

"""
    ),
    (
        TestCase(value_cls=elib_config.ConfigValuePath, path=('value',), run_after=['must_be_file', 'must_exist']),
        r"""# desc
# value type: path (must be a file, must already exist)
# WARNING: backslash characters ("\") must be doubled.
# Alternatively, you can use the forward slash: "/" (even on Windows).
# example = c:\\some\\folder
# example = c:\\some\\folder\\file.ext
# example = c:/this/is/valid/too
# MANDATORY CONFIG VALUE: you *must* provide a value for this setting
# 
value = 

"""
    ),
    (
        TestCase(value_cls=elib_config.ConfigValuePath, path=('value',), run_after=['must_be_dir', 'must_exist']),
        r"""# desc
# value type: path (must be a directory, must already exist)
# WARNING: backslash characters ("\") must be doubled.
# Alternatively, you can use the forward slash: "/" (even on Windows).
# example = c:\\some\\folder
# example = c:\\some\\folder\\file.ext
# example = c:/this/is/valid/too
# MANDATORY CONFIG VALUE: you *must* provide a value for this setting
# 
value = 

"""
    ),
    (
        TestCase(value_cls=elib_config.ConfigValueTableArray, path=('value',),
                 keys=(
                     elib_config.ConfigValueTableKey('key1', str, 'desc'),
                 )),
        """# desc
# value type: array of tables
# 
# Type of keys:
#     key name: key1
#     key type: string
#     desc
#     This key is MANDATORY
# 
# An array of tables is a list of table that share a common schema of key/value pairs.
# example:
#     [[value]]
#     key1 = "some text"
# 
# NOTE: the above example can be repeated as many times as needed, to create multiple tables in the array.
# MANDATORY CONFIG VALUE: you *must* provide a value for this setting
# 
value = 

"""
    ),
    (
        TestCase(value_cls=elib_config.ConfigValueTableArray, path=('value',),
                 keys=(
                     elib_config.ConfigValueTableKey('key1', str, 'desc', default='default key value'),
                 )),
        """# desc
# value type: array of tables
# 
# Type of keys:
#     key name: key1
#     key type: string
#     desc
#     This key is optional, and has a default value of: default key value
# 
# An array of tables is a list of table that share a common schema of key/value pairs.
# example:
#     [[value]]
#     key1 = "default key value"
# 
# NOTE: the above example can be repeated as many times as needed, to create multiple tables in the array.
# MANDATORY CONFIG VALUE: you *must* provide a value for this setting
# 
value = 

"""
    ),
    (
        TestCase(value_cls=elib_config.ConfigValueTableArray, path=('value',),
                 default=[{'key1': 'test'}],
                 keys=(
                     elib_config.ConfigValueTableKey('key1', str, 'desc', default='default key value'),
                 )),
        """# desc
# value type: array of tables
# 
# Type of keys:
#     key name: key1
#     key type: string
#     desc
#     This key is optional, and has a default value of: default key value
# 
# An array of tables is a list of table that share a common schema of key/value pairs.
# example:
#     [[value]]
#     key1 = "default key value"
# 
# NOTE: the above example can be repeated as many times as needed, to create multiple tables in the array.
# Setting this value is not required; you can leave it commented out.
# The default value (the one that will be used if you do not provide another) is shown below:
# 
# [[value]]
# key1 = "test"
# 
"""
    ),
]


@pytest.mark.parametrize('test_case, expected', TEST_DATA)
def test_config_values_to_text(test_case, expected):
    test_case.create()
    _config_example.write_example_config('test')
    _, content = pathlib.Path('test').read_text('utf8').split('# START OF ACTUAL CONFIG FILE')
    content = content.lstrip()
    test_file = pathlib.Path('test.toml')
    test_file.write_text(content, 'utf8')
    if test_case.default is not None:
        tomlkit.loads(test_file.read_text('utf8'))
    assert expected == content, content
