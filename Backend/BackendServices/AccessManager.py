# region HEADER
# !/usr/bin/env python
__author__ = "Lukas Klein"
__copyright__ = "Copyright 2021, The MUDCake Project"
__credits__ = "Hauke Presig, Jack Drillisch, Jan Gruchott, Lukas Klein, Robert Fendrich, Thomas Zimmermann"

__license__ = """MIT License

                     Copyright (c) 2021 MUDCake Project

                     Permission is hereby granted, free of charge, to any person obtaining a copy
                     of this software and associated documentation files (the "Software"), to deal
                     in the Software without restriction, including without limitation the rights
                     to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
                     copies of the Software, and to permit persons to whom the Software is
                     furnished to do so, subject to the following conditions:

                     The above copyright notice and this permission notice shall be included in all
                     copies or substantial portions of the Software.

                     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
                     IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
                     FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
                     AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
                     LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
                     OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
                     SOFTWARE."""

__version__ = "1.0.0"
__maintainer__ = "Lukas Klein"
__email__ = "mudcake@gmail.com"
__status__ = "Development"
# endregion
from DatabaseHandler.DatabaseHandler import *


class AccessManager:
    """ The Class AccessManager is there to manage the basic access of users to the dungeon.

    It contains a database handler for managing access to the database.
    """
    def __init__(self):
        self.db_handler = DatabaseHandler()

    def user_status_on_access_list(self, dungeon_id: str, user_name: str):
        """ This method calls the database and checks if the given user is on the access list.

        Args:
            dungeon_id (str): The dungeon id of the dungeon of the which is supposed to be checked.
            user_name (str): The name of the user which is supposed to be checked.

        Returns:
            True if the user is whitelisted, False if the user is blacklisted.
            None if the user is not listed on the access list.

        """
        ret = self.db_handler.user_status_on_access_list(user_name, dungeon_id)
        return bool(ret[0]) if ret else None
