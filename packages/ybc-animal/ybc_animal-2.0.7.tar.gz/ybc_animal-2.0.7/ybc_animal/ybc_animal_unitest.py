import unittest
from .ybc_animal import *


class MyTestCase(unittest.TestCase):
    def test_what(self):
        self.assertEqual('狗', what('test.jpg'))

    def test_breed(self):
        self.assertEqual('金毛犬', breed('test.jpg'))


if __name__ == '__main__':
    unittest.main()
