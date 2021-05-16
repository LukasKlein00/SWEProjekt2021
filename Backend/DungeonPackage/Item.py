#!/usr/bin/env python
__author__ = "Jan Gruchott"
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
__maintainer__ = "Jan Gruchott"
__email__ = "mudcake@gmail.com"
__status__ = "Development"

from DatabaseHandler.DatabaseHandler import *


class Item:
    def __init__(self, item_id: str= None, name: str= None, description: str= None, dungeon_id: str = None):
        self.item_id = item_id
        self.name = name
        self.description = description
        self.dungeon_id = dungeon_id

    def load_data(self, dungeonID):
        db_handler = DatabaseHandler()
        database_item = db_handler.get_item_by_dungeon_id(dungeonID)
        self.item_id = database_item[0]
        self.description = database_item[1]
        self.name = database_item[2]

    def to_dict(self):
        return {'itemID': self.item_id, 'name': self.name, 'description': self.description, 'dungeonID': self.dungeon_id}
