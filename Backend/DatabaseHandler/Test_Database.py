from DatabaseHandler import Test_DatabaseHandler_Mock
from Test_DatabaseHandler_Mock import MockDB
from mock import patch
import utils

class TestDatabaseHandler(MockDB):

    def test_Database(self):
        with self.mock_db_config:
            self.assertEqual(True, False)