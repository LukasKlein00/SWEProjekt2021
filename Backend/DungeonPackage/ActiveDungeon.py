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

from DungeonPackage.Character import Character
from DungeonPackage.Class import Class as Class
from DungeonPackage.DungeonData import DungeonData as DungeonData
from DungeonPackage.Item import Item as Item
from DungeonPackage.Npc import Npc as Npc
from DungeonPackage.Race import Race as Race
from DungeonPackage.Room import Room as Room
from DatabaseHandler.DatabaseHandler import DatabaseHandler


class ActiveDungeon:
    """
    class for handling active dungeons
    """
    def __init__(self, user_ids: [str] = None, character_ids: [str] = None, rooms: [Room] = None, npcs: [Npc] = None,
                 items: [Item] = None, races: [Race] = None,
                 classes: [Class] = None, dungeon_data: DungeonData = None):
        """
        constructor for ActiveDungeon class
        """
        self.user_ids = user_ids
        self.character_ids = character_ids
        self.rooms = [rooms]
        self.rooms_objects = []
        self.npcs = npcs
        self.items = items
        self.races = races
        self.classes = classes
        self.dungeon_data = dungeon_data
        self.db_handler = DatabaseHandler()

    def add_item(self, item: Item):
        """
        adds an item to activeDungeon
        :param item: item object
        """
        self.items.append(item)

    def add_race(self, race: Race):
        """
        adds an race to activeDungeon
        :param race: race object
        """
        self.races.append(race)

    def is_dungeon_master_in_game(self) -> bool:
        """
        checks if dungeon master is in game
        :param item: item object
        :return: True if so
        """
        return self.user_ids.contains(self.dungeon_data.dungeon_master_id)

    def add_room(self, room: Room):
        """
        adds an room to activeDungeon
        :param room: room object
        """
        self.rooms.append(room)

    def add_class(self, d_class: Class):
        """
        adds an class to activeDungeon
        :param item: item object
        """
        self.classes.append(d_class)

    def add_character(self, character: Character):
        """ adds a character object to the active dungeon

        Args:
            character (Character): character to be added to the active dungeon

        Returns: void
        """
        self.character_ids.append(character.character_id)

    def load_data(self):
        raise NotImplementedError

    def change_race_visibility(self):
        raise NotImplementedError

    def change_class_visibility(self):
        raise NotImplementedError

    def move_character(self):
        raise NotImplementedError

    def load_rooms(self, dungeon_id):
        rooms_dict = self.db_handler.get_all_rooms_by_dungeon_id_as_dict(dungeon_id=dungeon_id)
        for room_dict in rooms_dict:
            room = {'roomID': room_dict['roomID'], 'name': room_dict['roomName'], 'isStartRoom': room_dict['isStartRoom'],
                     'description': room_dict['roomDescription'], 'x': room_dict['x'], 'y': room_dict['y'],
                     'north': room_dict['north'],'east':room_dict['east'], 'south':room_dict['south'],
                     'west': room_dict['west'], 'npc': {'npcID': room_dict['npcID'], 'name': room_dict['npcName'],
                                                        'description': room_dict['npcDescription'], 'equipment': {'itemID': room_dict['npcItemID'],
                                                                                                                  'name': room_dict['npcItemName'],
                                                                                                                  'description': room_dict['npcItemDesc']}},
                     'item': {'itemID': room_dict['roomItemID'], 'name': ['roomItemName'], 'description': room_dict['roomItemDescription']}}
            self.rooms.append(room)

        self.__parse_rooms(rooms_dict)

    def __parse_rooms(self, room_dict):
        for room in room_dict:
            done_room = Room(room_id=room['roomID'], room_name=room['roomName'], is_start_room=room['isStartRoom'],
                             room_description=room['roomDescription'], coordinate_x=room['x'], coordinate_y=room['y'],
                             north=room['north'], east=room['east'], south=room['south'], west=room['west'])
            self.rooms_objects.append(done_room)
