#!/usr/bin/env python
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

from DungeonPackage.AccessList import AccessList as AccessList
from DatabaseHandler.DatabaseHandler import *


class DungeonData:
    def __init__(self, dungeon_id: str = None, dungeon_master_id: str = None, max_players: int = None, name: str = None,
                 description: str = None,
                 private: bool = False, access_list: AccessList = None):
        self.dungeon_id = dungeon_id
        self.dungeon_master_id = dungeon_master_id
        self.max_players = max_players
        self.name = name
        self.description = description
        self.private = private
        self.access_list = access_list



    def is_dungeon_master_in(self):
        raise NotImplementedError

    def add_room(self):
        raise NotImplementedError

    def add_item_to_room(self):
        raise NotImplementedError

    def add_npc_to_room(self):
        raise NotImplementedError

    def load_data(self, dungeon_id: str):
        db_handler = DatabaseHandler()
        database_dungeon_data_raw = db_handler.get_dungeon_data_by_dungeon_id(dungeon_id)
        database_dungeon_data = list(sum(database_dungeon_data_raw, ()))
        self.dungeon_id = database_dungeon_data[0]
        self.max_players = database_dungeon_data[5]
        self.name = database_dungeon_data[2]
        self.description = database_dungeon_data[3]
        self.private = bool(database_dungeon_data[4])
        self.dungeon_master_id = database_dungeon_data[1]
        return self

        return self

    def is_private(self):
        raise NotImplementedError

    def overwrite_dungeon_master_id(self):
        raise NotImplementedError

