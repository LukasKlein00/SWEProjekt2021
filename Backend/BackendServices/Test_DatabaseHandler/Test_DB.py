import unittest
from Test_DatabaseHandler_Mock import MockDB


class MyTestCase(MockDB):
    def test_something(self):
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
