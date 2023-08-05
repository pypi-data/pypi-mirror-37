import unittest
from ybc_imgcar import *

class MyTestCase(unittest.TestCase):
    def test_car_recognition(self):
        self.assertEqual('阿斯顿马丁DBS', car_recognition('test.jpg'))


if __name__ == '__main__':
    unittest.main()
