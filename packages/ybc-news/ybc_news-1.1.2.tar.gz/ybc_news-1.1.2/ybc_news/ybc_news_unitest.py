import unittest
from ybc_news import *

class MyTestCase(unittest.TestCase):
    def test_channels(self):
        list = ['头条', '社会', '国内', '国际', '娱乐', '体育', '军事', '科技', '财经', '时尚']
        self.assertEqual(list, channels())

    def test_news(self):
        self.assertIsNotNone(news('头条'))

if __name__ == '__main__':
    unittest.main()
