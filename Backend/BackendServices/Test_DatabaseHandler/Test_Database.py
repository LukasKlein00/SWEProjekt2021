import unittest
from Test_DatabaseHandler_Mock import MockDB
from unittest import mock


class TestDatabaseHandler(MockDB):

    def test_register_user(self):
        with self.mock_db_config:
            self.assertEqual(True, False)
