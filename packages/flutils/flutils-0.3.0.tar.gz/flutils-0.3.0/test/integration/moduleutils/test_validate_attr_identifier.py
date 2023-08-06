import unittest
import keyword
from flutils.moduleutils import (
    _validate_attr_identifier,
    _DUNDERS,
)


class Test(unittest.TestCase):

    def test_integration_validate_attr_identifier(self):
        val = _validate_attr_identifier('foo', 'line')
        self.assertEqual(val, 'foo')

    def test_integration_validate_attr_identifier_keyword_error(self):
        for name in keyword.kwlist:
            msg = f"name={name!r}"
            with self.assertRaises(AttributeError, msg=msg):
                _validate_attr_identifier(name, 'line')

    def test_integration_validate_attr_identifier_builtins_error(self):
        for name in tuple(dir('__builtins__')):
            msg = f"name={name!r}"
            with self.assertRaises(AttributeError, msg=msg):
                _validate_attr_identifier(name, 'line')

    def test_integration_validate_attr_identifier_dunders_error(self):
        for name in _DUNDERS:
            msg = f"name={name!r}"
            with self.assertRaises(AttributeError, msg=msg):
                _validate_attr_identifier(name, 'line')

