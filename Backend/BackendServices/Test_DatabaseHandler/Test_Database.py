import unittest
from Test_DatabaseHandler_Mock import MockDB
from unittest import mock


class TestDatabaseHandler(unittest.TestCase):

    def test_register_user(self, mock_db_config):
        self.assertEqual(True, False)
