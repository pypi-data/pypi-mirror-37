import unittest
from ybc_carbrand import *


class MyTestCase(unittest.TestCase):
    def test_brands(self):
        self.assertIsNotNone(brands())


if __name__ == '__main__':
    unittest.main()
