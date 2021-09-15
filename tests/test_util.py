import unittest

from hacksoc_org.util import removeprefix, removesuffix

class TestFreeze(unittest.TestCase):

    def test_prefix(self):
        self.assertEqual(removeprefix("Hello, World!", ""), "Hello, World!")
        self.assertEqual(removeprefix("Hello, World!", "Hello"), ", World!")
        self.assertEqual(removeprefix("Hello, World!", "Hello, World!"), "")
        self.assertEqual(removeprefix("Hello, World!", "ello,"), "Hello, World!")

        self.assertEqual(removeprefix("", "Hello"), "")
        self.assertEqual(removeprefix("Hello", "Hello, World!"), "Hello")

    def test_suffix(self):
        self.assertEqual(removesuffix("Hello, World!", ""), "Hello, World!")
        self.assertEqual(removesuffix("Hello, World!", "World!"), "Hello, ")
        self.assertEqual(removesuffix("Hello, World!", "Hello, World!"), "")
        self.assertEqual(removesuffix("Hello, World!", "World"), "Hello, World!")
        
        self.assertEqual(removesuffix("", "World!"), "")
        self.assertEqual(removesuffix("World!", "Hello, World!"), "World!")