from DatabaseHandler import Test_DatabaseHandler_Mock
from Test_DatabaseHandler_Mock import MockDB
import unittest
from mock import patch
import utils


class TestDatabaseHandler(MockDB):

    def test_registerUser(self):
        with self.mock_db_config:
            self.assertEqual(True, False)
