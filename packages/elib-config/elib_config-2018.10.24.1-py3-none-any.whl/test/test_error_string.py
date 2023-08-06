# coding=utf-8

import elib_config
from pathlib import Path

_TOML_TEXT = """
[container1]
key1 = "value1"
int1 = 1
float1 = 1.0
list1 = ["list", "of", "string"]
"""

KEY1 = elib_config.ConfigValueString('container1', 'key1', description='')
INT1 = elib_config.ConfigValueInteger('container1', 'int1', description='')
FLOAT1 = elib_config.ConfigValueFloat('container1', 'float1', description='')
LIST1 = elib_config.ConfigValueList('container1', 'list1', description='', element_type=str)


def test_basics():
    Path('config.toml').write_text(_TOML_TEXT)
    assert KEY1() == 'value1'
    assert INT1() == 1
    assert FLOAT1() == 1.0
    assert LIST1() == ['list', 'of', 'string']
