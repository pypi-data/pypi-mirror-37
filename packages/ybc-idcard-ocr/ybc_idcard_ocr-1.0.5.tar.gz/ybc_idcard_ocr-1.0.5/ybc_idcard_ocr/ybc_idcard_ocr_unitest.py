import unittest
from ybc_idcard_ocr import *

class MyTestCase(unittest.TestCase):
    def test_idcard_infor(self):
        res = {'name': '二哈', 'sex': '男', 'nation': '汉', 'birth': '2015/3/8', 'address': '河南省安阳市文峰区', 'id': '410502201503081234'}
        self.assertEqual(res, idcard_info('test.jpg'))


if __name__ == '__main__':
    unittest.main()
