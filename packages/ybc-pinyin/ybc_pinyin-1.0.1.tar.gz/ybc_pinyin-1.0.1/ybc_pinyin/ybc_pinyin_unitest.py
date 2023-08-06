import unittest
from ybc_pinyin import *


class MyTestCase(unittest.TestCase):
    def test_pin(self):
        self.assertEqual('nǐ-hǎo', pin('你好'))

    def test_pin1(self):
        self.assertEqual('ni-hao', pin1('你好'))

    def test_pin(self):
        self.assertEqual('chē-jū', duoyin('车'))


if __name__ == '__main__':
    unittest.main()
