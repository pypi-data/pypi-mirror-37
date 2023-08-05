import re
from unittest import TestCase

from pythonUtils import converter


class TestConverter(TestCase):
    def test_converter(self):
        self.assertEqual(converter.to_int("27"), 27)
        self.assertEqual(converter.to_int("__27", regex=True), 27)
        self.assertEqual(converter.to_int("00abc21xyz42", regex=True), 42)
        self.assertEqual(converter.to_int("00abc21xyz42", regex=True, match_group_index=0), 0)
        self.assertEqual(converter.to_int("00abc21xyz42", regex=True, match_group_index=1), 21)
        self.assertEqual(converter.to_int("1234567890", regex="(\d{2})"), 90)
        self.assertEqual(converter.to_int("abc_42_xyz", regex=re.compile("(\d{2})")), 42)
        with self.assertRaises(TypeError):
            converter.to_int("test123", regex={})

        self.assertEqual(converter.to_int("test"), 0)
        self.assertEqual(converter.to_int("test", default=25), 25)

        with self.assertRaises((ValueError, TypeError)):
            converter.to_int("abc", exception=())

        with self.assertRaises(IndexError):
            converter.to_int("0,1,2", regex=True, match_group_index=25)

    def test_convert_float(self):
        self.assertEqual(converter.to_float("12.3"), 12.3)
        self.assertEqual(converter.to_float("12"), 12)
        self.assertEqual(converter.to_float("ab12.0", regex=True), 12.0)
        self.assertEqual(converter.to_float("ab12.3", regex=True), 12.3)
        self.assertEqual(converter.to_float("abcd"), 0)
        self.assertIsInstance(converter.to_float("abc"), float)
