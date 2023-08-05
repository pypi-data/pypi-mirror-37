import unittest
from ybc_namecard import *

class MyTestCase(unittest.TestCase):
    def test_namecard_info(self):
        res = {'姓名': '何山', '职位': '研发总监', '地址': '0北京市朝阳区望京利星行中心A座F区6层', '邮箱': 'heshan@fenbi.com', '手机': '18635579617'}
        self.assertEqual(res, namecard_info('test.jpg'))


if __name__ == '__main__':
    unittest.main()
