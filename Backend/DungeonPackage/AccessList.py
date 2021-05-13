#!/usr/bin/env python
__author__ = "Thomas Zimmermann"
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
__maintainer__ = "Thomas Zimmermann"
__email__ = "mudcake@gmail.com"
__status__ = "Development"

from DatabaseHandler.DatabaseHandler import DatabaseHandler


class AccessList:
    """
    class for handling access list
    """

    def __init__(self, dungeon_id: str = None):
        """
        constructor for class AccessList
        """
        self.access_list = []
        self.dungeon_id = dungeon_id

    def add_user_to_access_list(self, user_name: str, is_allowed: bool):
        """
        adds a user to AccessList
        :param user_id: id of user
        :param is_allowed: bool true=user on white list false=user on blacklist  
        """
        self.access_list.append({"user_name": user_name, "is_allowed":is_allowed})

    def load_data(self):
        """Part of the lazy loading process.
        Fills the AccessList class with data from the database.

        Returns:
            void: This Method only fills its own parameters
        """
        db_handler = DatabaseHandler()
        for user in db_handler.get_access_list_by_dungeon_id(self.dungeon_id):
            self.access_list.append({"user_name": user['userName'], "is_allowed": bool(user['isAllowed'])})
        return self