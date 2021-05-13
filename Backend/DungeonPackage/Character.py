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

from DatabaseHandler.DatabaseHandler import DatabaseHandler
from DungeonPackage.Inventory import *


class Character:
    def __init__(self, life_points: int = 100, name: str = None, description: str = None, class_id: int = None, race_id: int = None,
                 user_id: str = None, room_id: str = None, inventory: Inventory = None, dungeon_id: str = None, discovered_rooms: [str] = [], character_id:str = None):
        self.life_points = life_points
        self.name = name
        self.description = description
        self.class_id = class_id
        self.race_id = race_id
        self.user_id = user_id
        self.room_id = room_id
        self.inventory = inventory
        self.dungeon_id = dungeon_id
        self.character_id = character_id
        self.discovered_rooms = discovered_rooms
        self.db_handler = DatabaseHandler()

    def load_data(self, user_id: str, dungeon_id: str):
        db_handler = DatabaseHandler()
        try:
            databaseCharacterData = db_handler.get_character_by_user_id(user_id, dungeon_id)
            self.life_points = databaseCharacterData["Lifepoints"]
            self.name = databaseCharacterData["CharacterName"]
            self.description = databaseCharacterData["CharacterDescription"]
            self.class_id = databaseCharacterData["ClassID"]
            self.race_id = databaseCharacterData["RaceID"]
            self.user_id = user_id
            #TODO: self.discovered_map = databaseCharacterData["RoomID"]
            self.dungeon_id = dungeon_id
            return self
        except:
            print("Ich bin eine exception")
            return None

    def add_item_to_inventory(self, item_id: str):
        self.db_handler.add_item_to_inventory(item_id, self.user_id, self.dungeon_id)

    def to_dict(self):
        return {'characterID': self.character_id, 'name': self.name, 'description': self.description,
                'health': self.life_points, 'classID': self.class_id, 'raceID': self.race_id,
                'userID': self.user_id, 'roomID': self.room_id, 'inventory': self.db_handler.get_inventory_by_dungeon_user_id(self.dungeon_id, self.user_id)}
