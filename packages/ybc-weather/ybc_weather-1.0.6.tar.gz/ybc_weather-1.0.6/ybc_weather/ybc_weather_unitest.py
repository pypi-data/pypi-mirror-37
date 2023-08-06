import unittest
from ybc_weather import *


class MyTestCase(unittest.TestCase):
    def test_something(self):
        test1 = today('北京')
        test2 = today('北京')
        self.assertEqual(test1, test2)


if __name__ == '__main__':
    unittest.main()