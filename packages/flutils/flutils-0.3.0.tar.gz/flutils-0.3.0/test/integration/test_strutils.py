import unittest

# noinspection PyUnresolvedReferences
from flutils import (
    camel_to_underscore,
    underscore_to_camel
)


class TestCamelToUnderscore(unittest.TestCase):

    def test_integration_camel_to_underscore_foo_bar(self):
        data = camel_to_underscore('FooBar')
        self.assertEqual(data, 'foo_bar')

    def test_integration_camel_to_underscore_one_two(self):
        data = camel_to_underscore('oneTwo')
        self.assertEqual(data, 'one_two')

    def test_integration_camel_to_underscore_three_four_five(self):
        data = camel_to_underscore('THREEFourFive')
        self.assertEqual(data, 'three_four_five')

    def test_integration_camel_to_underscore_six_seven_eight(self):
        data = camel_to_underscore('sixSEVENEight')
        self.assertEqual(data, 'six_seven_eight')

    def test_integration_camel_to_underscore_nine_ten_eleven(self):
        data = camel_to_underscore('NINETenELEVEN')
        self.assertEqual(data, 'nine_ten_eleven')


class TestUnderscoreToCamel(unittest.TestCase):

    def test_integration_underscore_to_camel_foo_bar(self):
        data = underscore_to_camel('foo_bar', lower_first=True)
        self.assertEqual(data, 'fooBar')

    def test_integration_underscore_to_camel_one_two(self):
        data = underscore_to_camel('one__two', lower_first=False)
        self.assertEqual(data, 'OneTwo')

    def test_integration_underscore_to_camel_three_four(self):
        data = underscore_to_camel('three__four__', lower_first=True)
        self.assertEqual(data, 'threeFour')

    def test_integration_underscore_to_camel_five_six(self):
        data = underscore_to_camel('__five_six__', lower_first=False)
        self.assertEqual(data, 'FiveSix')

