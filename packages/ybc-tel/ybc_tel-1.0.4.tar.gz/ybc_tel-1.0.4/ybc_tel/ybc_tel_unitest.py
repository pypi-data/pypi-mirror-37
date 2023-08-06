import unittest
from .ybc_tel import *

class MyTestCase(unittest.TestCase):
    def test_detail(self):
        self.assertEqual({'province': '山西', 'city': '太原', 'company': '联通', 'shouji': '18635579617'}, detail(18635579617))


if __name__ == '__main__':
    unittest.main()
