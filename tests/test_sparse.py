import unittest
from sparse import parse

class TestSparse(unittest.TestCase):
    def test_parse_basic(self):
        result = parse("Hello World!")
        self.assertEqual(result, "Hello World!")

# TODO: Add more tests