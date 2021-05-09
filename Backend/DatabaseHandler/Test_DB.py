import unittest
from DatabaseHandler import Test_DatabaseHandler_Mock
from Test_DatabaseHandler_Mock import MockDB
from mock import patch
import utils


class MyTestCase(MockDB):
    def test_something(self):
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
