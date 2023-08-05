import unittest
from ybc_trans import *


class MyTestCase(unittest.TestCase):
    def test_zh2en(self):
        self.assertEqual('test', zh2en('测试'))

    def test_en2zh(self):
        self.assertEqual('苹果', en2zh('apple'))


if __name__ == '__main__':
    unittest.main()
