import unittest
from ybc_food import *

class MyTestCase(unittest.TestCase):
    def test_check(self):
        self.assertEqual(True, check('test.jpg'))

    def test_food_name(self):
        self.assertEqual('汉堡', food_name('test.jpg'))

if __name__ == '__main__':
    unittest.main()
