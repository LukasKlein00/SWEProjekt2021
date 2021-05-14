# region HEADER
# !/usr/bin/env python
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
# endregion
import json
import uuid
import logging
import sys

from DatabaseHandler.DatabaseHandler import DatabaseHandler
from DungeonPackage.AccessList import AccessList
from DungeonPackage.ActiveDungeon import ActiveDungeon
from DungeonPackage.Character import Character
from DungeonPackage.Class import Class
from DungeonPackage.DungeonData import DungeonData
from DungeonPackage.Item import Item
from DungeonPackage.Npc import Npc
from DungeonPackage.Race import Race
from DungeonPackage.Room import Room


class DungeonManager:
    """ Main class for handling everything dungeon based

    """

    def __init__(self, data=None):
        """

        Args:
            data (json, optional): A JSON Object which contains all necessary information for a dungeon
                                    - List of all Rooms which are saved as an dictionary
                                    - List of all Races which are saved as an dictionary
                                    - List of all Classes which are saved as an dictionary
                                    - List of all Items which are saved as an dictionary
                                    - List of all Npcs which are saved as an dictionary
                                    - Accesslist which contains all users which are saved on there
        """
        self.managed_dungeon = DungeonData()
        logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
        self.data = data

        self.db_handler = DatabaseHandler()
        self.room_list = []
        self.race_list = []
        self.class_list = []
        self.item_list = []
        self.npc_list = []
        self.accesslist = []
        self.fill_attributes(data)

    def fill_attributes(self, data):
        """ Fills attributes which may not be given in the init

        Args:
            data (json, optional): A JSON Object which contains all necessary information for a dungeon
                                    - List of all Rooms which are saved as an dictionary
                                    - List of all Races which are saved as an dictionary
                                    - List of all Classes which are saved as an dictionary
                                    - List of all Items which are saved as an dictionary
                                    - List of all Npcs which are saved as an dictionary
                                    - Accesslist which contains all users which are saved on there

        """
        if data:

            self.managed_dungeon = DungeonData(dungeon_id=self.data['dungeonID'],
                                               dungeon_master_id=self.data['dungeonMasterID'],
                                               max_players=self.data['maxPlayers'],
                                               name=self.data['dungeonName'],
                                               description=self.data['dungeonDescription'],
                                               private=self.data['private'],
                                               access_list=AccessList(data['dungeonID']))

            self.check_for_dungeon_id()
            logging.debug("constructor: " + self.managed_dungeon.dungeon_id)
            self.parse_config_data()
        else:
            logging.debug("data is none")

    def parse_config_data(self):
        """ Parses the config data of every json list into an Object

        """

        race_data = self.data['races']
        items_data = self.data['items']
        npcs_data = self.data['npcs']
        room_data = self.data['rooms']
        class_data = self.data['classes']
        accesslist_data = self.data['accessList']

        for race in race_data:
            logging.debug(race)

            new_race = Race(name=race['name'], description=race['description'],
                            dungeon_id=self.managed_dungeon.dungeon_id)

            check_for_race_id = 'raceID' in race
            if check_for_race_id:
                new_race.race_id = race['raceID']
            else:
                new_race.race_id = str(uuid.uuid4())
            self.race_list.append(new_race)

        for item in items_data:
            logging.debug(item)
            new_item = Item(name=item['name'], description=item['description'])
            new_item.item_id = item['itemID'] if 'itemID' in item else str(uuid.uuid4())
            self.item_list.append(new_item)

        for npc in npcs_data:
            logging.debug(npc)
            new_npc = Npc(npc_id=npc['npcID'], name=npc['name'],
                          description=npc['description'], dungeon_id=self.managed_dungeon.dungeon_id)
            new_npc.item = None if npc['equipment'] is None else npc['equipment']['itemID']
            self.npc_list.append(new_npc)

        for classes in class_data:
            logging.debug(classes)
            new_class = Class(name=classes['name'], description=classes['description'],
                              dungeon_id=self.managed_dungeon.dungeon_id)

            check_for_class_id = 'classID' in classes
            if check_for_class_id:
                new_class.class_id = classes['classID']
            else:
                new_class.class_id = str(uuid.uuid4())

            if classes['equipment'] is None:
                new_class.item_id = None
            else:
                new_class.item_id = classes['equipment']['itemID']
                logging.debug(classes['equipment']['itemID'])
            self.class_list.append(new_class)

        for room in room_data:
            logging.debug(room)
            new_room = Room(coordinate_x=room['x'], coordinate_y=room['y'], north=room['north'], east=room['east'],
                            south=room['south'], west=room['west'], dungeon_id=self.managed_dungeon.dungeon_id)

            check_for_room_id = 'roomID' in room
            if check_for_room_id:
                new_room.room_id = room['roomID']
                logging.debug("roomID assigned")
            else:
                new_room.room_id = str(uuid.uuid4())
                logging.debug("roomID generated")

            check_for_name = 'name' in room
            if check_for_name:
                new_room.room_name = room['name']
            else:
                new_room.room_name = None

            check_for_description = 'description' in room
            if check_for_description:
                new_room.room_description = room['description']
            else:
                new_room.room_description = None

            check_for_start_room = 'isStartRoom' in room
            if check_for_start_room:
                new_room.is_start_room = room['isStartRoom']
            else:
                new_room.is_start_room = False

            check_for_npc = 'npc' in room
            if check_for_npc:
                new_room.npc_id = room['npc']['npcID']
            else:
                new_room.npc_id = None

            check_for_item = 'item' in room
            if check_for_item:
                new_room.item_id = room['item']['itemID']
            else:
                new_room.item_id = None

            self.room_list.append(new_room)

        for ac_l in accesslist_data:
            self.managed_dungeon.access_list.add_user_to_access_list(user_name=ac_l['name'],
                                                                     is_allowed=ac_l['isAllowed'])

    def write_dungeon_to_database(self):
        """ Writes the dungeon to the database.

        All data which gets used here is from the already initialised object

        """
        active_dungeon = ActiveDungeon(rooms=self.room_list, classes=self.class_list, npcs=self.npc_list,
                                       items=self.item_list, dungeon_data=self.managed_dungeon, races=self.race_list,
                                       user_ids=None, character_ids=None)
        try:
            self.db_handler.save_or_update_dungeon(active_dungeon)
            logging.debug("Dungeon saved")
            self.__write_races_to_database()
            logging.debug("Races saved")
            self.__write_items_to_database()
            logging.debug("Item saved")
            self.__write_classes_to_database()
            logging.debug("Classes saved")
            self.__write_npcs_to_database()
            logging.debug("Npcs saved")
            self.__write_rooms_to_database()
            logging.debug("Rooms saved")
            logging.debug("write dungeon to database: self.managed_dungeon.dungeon_id")
            self.write_accesslist_to_database()
            return self.managed_dungeon.dungeon_id
        except IOError:
            pass

    def check_for_dungeon_id(self):
        """ Checks if the user already has an id

        If not the methods creates one and sets it as the dungeon id of the managed dungeon

        """
        if self.managed_dungeon.dungeon_id is None:
            self.managed_dungeon.dungeon_id = str(uuid.uuid4())

    def __write_races_to_database(self):
        """ Private method that writes a list of races to the database via the database handler

        """
        logging.debug(self.race_list)
        for race in self.race_list:
            try:
                self.db_handler.write_race_to_database(race=race, dungeon_id=self.managed_dungeon.dungeon_id)
            except IOError:
                pass

    def __write_classes_to_database(self):
        """ Private method that writes a list of classes to the database via the database handler

        """
        logging.debug(self.class_list)
        for classes in self.class_list:
            try:
                self.db_handler.write_class_to_database(class_object=classes,
                                                        dungeon_id=self.managed_dungeon.dungeon_id)
            except IOError:
                pass

    def __write_rooms_to_database(self):
        """ Private method that writes a list of rooms to the database via the database handler

        """
        logging.debug(self.room_list)
        for room in self.room_list:
            try:
                self.db_handler.write_room_to_database(room=room, dungeon_id=self.managed_dungeon.dungeon_id)
            except IOError:
                pass

    def write_character_to_database(self, character: Character):
        """ writes a given character to the database

        Args:
            character (Character): character to be written to the database

        Returns: void
        """
        try:
            self.db_handler.write_character_to_database(character, character.dungeon_id)
        except IOError:
            pass

    def __write_items_to_database(self):
        """ Private method that writes a list of items to the database via the database handler

        """
        logging.debug(self.item_list)
        for item in self.item_list:
            try:
                self.db_handler.write_item_to_database(item=item, dungeon_id=self.managed_dungeon.dungeon_id)
            except IOError:
                pass

    def __write_npcs_to_database(self):
        """ Private method that writes a list of npcs to the database via the database handler

        """
        logging.debug(self.npc_list)
        for npc in self.npc_list:
            try:
                self.db_handler.write_npc_to_database(npc=npc, dungeon_id=self.managed_dungeon.dungeon_id)
            except IOError:
                pass

    def write_accesslist_to_database(self):
        """ Private method that writes a list of users in the accesslist to the database via the database handler

        """
        for user in self.managed_dungeon.access_list.access_list:
            self.db_handler.write_user_to_acceslist(access_list_user=user, dungeon_id=self.managed_dungeon.dungeon_id)

    def get_dungeon_by_id(self, user_id_data):
        """ Gets the dungeons via the user id

        Args:
            user_id_data (str): The user id which holds the dungeons

        Returns:
            All dungeons which the user has created

        """
        return self.db_handler.get_dungeon_by_id(user_id_data)

    def get_dungeon_data_by_dungeon_id(self, dungeon_id):
        """ Retrieves first glance data of the dungeon via the id

        Args:
            dungeon_id (str): Dungeon of the dungeon id which needs data

        Returns:
            DungeonID, DungeonMasterID, DungeonName, DungeonDescription, the private status
            and the max players of the given dungeon

        """
        return self.db_handler.get_dungeon_data_by_dungeon_id(dungeon_id)

    def delete_dungeon(self, dungeon_id):
        """ Deletes a dungeon via the id in the database

        Args:
            dungeon_id (str): The dungeon id which is supposed to be deleted

        """
        try:
            self.db_handler.delete_dungeon_by_id(dungeon_id)
        except IOError:
            pass

    def copy_dungeon(self, dungeon_id):
        """ Copy's a given dungeon via the dungeon id

        Args:
            dungeon_id (str): The dungeon which is supposed to be copied

        """
        self.room_list = []
        self.race_list = []
        self.class_list = []
        self.item_list = []
        self.npc_list = []
        try:
            dungeon = self.db_handler.get_dungeon_data_by_dungeon_id(dungeon_id)
            logging.debug("Dungeon: ", dungeon)
            self.managed_dungeon.dungeon_id = str(uuid.uuid4())
            self.managed_dungeon.dungeon_master_id = dungeon[0][1]
            self.managed_dungeon.name = dungeon[0][2] + " - copy"
            self.managed_dungeon.description = dungeon[0][3]
            self.managed_dungeon.private = dungeon[0][4]
            self.managed_dungeon.max_players = dungeon[0][5]

            items = self.db_handler.get_item_by_dungeon_id(dungeon_id)
            for item in items:
                copied_item = Item(item_id=item[0], name=item[1], description=item[2],
                                   dungeon_id=self.managed_dungeon.dungeon_id)
                self.item_list.append(copied_item)

            logging.debug("Item List: ")
            logging.debug(self.item_list)

            rooms = self.db_handler.get_all_rooms_by_dungeon_id_as_dict(dungeon_id)
            for room in rooms:
                copied_room = Room(room_id=room['roomID'], room_name=room['roomName'],
                                   room_description=room['roomDescription'],
                                   coordinate_x=room['x'], coordinate_y=room['y'], north=room['north'],
                                   east=room['east'], south=room['south'], west=room['west'],
                                   is_start_room=room['isStartRoom'], npc_id=room['npcID'], item_id=room['roomItemID'],
                                   dungeon_id=self.managed_dungeon.dungeon_id)
                self.room_list.append(copied_room)
            logging.debug("Room List:")
            logging.debug(self.room_list)

            races = self.db_handler.get_race_by_dungeon_id(dungeon_id)
            for race in races:
                copied_race = Race(race_id=race[0], name=race[1], description=race[2],
                                   dungeon_id=self.managed_dungeon.dungeon_id)
                self.race_list.append(copied_race)
            logging.debug("Race List:")
            logging.debug(self.race_list)

            classes = self.db_handler.get_class_by_dungeon_id(dungeon_id)
            for class_tuple in classes:
                copied_class = Class(class_id=class_tuple[0], name=class_tuple[1], description=class_tuple[2],
                                     dungeon_id=self.managed_dungeon.dungeon_id)
                self.class_list.append(copied_class)

            logging.debug("Class List:")
            logging.debug(self.class_list)

            npcs = self.db_handler.get_npc_by_dungeon_id(dungeon_id)
            for npc in npcs:
                copied_npc = Npc(npc_id=npc[0], name=npc[1], description=npc[2], item=npc[3],
                                 dungeon_id=self.managed_dungeon.dungeon_id)
                self.npc_list.append(copied_npc)

            logging.debug("NPC List:")
            logging.debug(self.npc_list)

            # TODO: AccessList
            self.write_dungeon_to_database()

        except IOError:
            pass

    def get_start_rooms_in_dungeon(self, dungeon_id: str):
        """ Gets all start rooms of a dungeon based on the dungeon id

        Args:
            dungeon_id (str): Dungeon id of the dungeon

        Returns:
            All starting rooms in a dungeon
        """
        all_starting_rooms = []
        for room in self.get_all_from_room_as_json(dungeon_id):
            if room['isStartRoom']:
                all_starting_rooms.append(room)
        return all_starting_rooms

    def get_all_from_room_as_json(self, data):
        """ Gets all room data as json from dungeon id

        Args:
            data (str): Dungeon id of the dungeon

        Returns:
            All Rooms in the dungeon as list
        """
        rooms_dict = self.db_handler.get_all_rooms_by_dungeon_id_as_dict(dungeon_id=data)
        room_list = []
        for room_dict in rooms_dict:
            room = {'roomID': room_dict['roomID'], 'name': room_dict['roomName'],
                    'isStartRoom': room_dict['isStartRoom'],
                     'description': room_dict['roomDescription'], 'x': room_dict['x'], 'y': room_dict['y'],
                     'north': room_dict['north'], 'east': room_dict['east'], 'south': room_dict['south'],
                     'west': room_dict['west'], 'npc': {'npcID': room_dict['npcID'], 'name': room_dict['npcName'],
                                                        'description': room_dict['npcDescription'],
                                                        'equipment': {'itemID': room_dict['npcItemID'],
                                                                      'name': room_dict['npcItemName'],
                                                                      'description': room_dict['npcItemDesc']}},
                     'item': {'itemID': room_dict['roomItemID'], 'name': ['roomItemName'],
                              'description': room_dict['roomItemDescription']}}
            room_list.append(room)
        logging.debug(room_list)
        return room_list

    def get_all_from_classes_as_json(self, data):
        """ Gets all classes as json from dungeon id

        Args:
            data (str): Dungeon id of the dungeon

        Returns:
            All Classes in the dungeon as list
        """
        classes_dict = self.db_handler.get_all_classes_by_dungeon_id_as_dict(dungeon_id=data)
        class_list = []
        for class_dict in classes_dict:
            class_data = {'classID': class_dict['classID'], 'name': class_dict['name'],
                          'description': class_dict['description'],
                          'equipment': {'itemID': class_dict['itemID'], 'name': class_dict['itemName'],
                                        'description': class_dict['itemDescription']}}
            class_list.append(class_data)
        logging.debug(class_list)
        return class_list

    def get_all_from_races_as_json(self, data):
        """ Gets all races as json from dungeon id

        Args:
            data (str): Dungeon id of the dungeon

        Returns:
            All Races in the dungeon as list
        """
        races = self.db_handler.get_all_races_by_dungeon_id_as_dict(dungeon_id=data)
        logging.debug(races)
        return races

    def get_all_from_items_as_json(self, data):
        """ Gets all items as json from dungeon id

        Args:
            data (str): Dungeon id of the dungeon

        Returns:
            All items in the dungeon as JSON
        """
        items = self.db_handler.get_all_item_by_dungeon_id_as_dict(dungeon_id=data)
        logging.debug(items)
        return json.dumps(items).encode(encoding='utf_8')

    def get_all_from_npcs_as_json(self, data):
        npcs_dict = self.db_handler.get_all_npc_by_dungeon_id_as_dict(dungeon_id=data)
        npc_list = []
        for npc_dict in npcs_dict:
            npc = {'npcID': npc_dict['npcID'], 'name': npc_dict['name'], 'description': npc_dict['description'],
                   'equipment': {'itemID': npc_dict['itemID'], 'name': npc_dict['itemName'],
                                 'description': npc_dict['itemDescription']}
                   }
            npc_list.append(npc)
        logging.debug(npc_list)
        return json.dumps(npc_list).encode(encoding='utf_8')

    def get_character_config(self, data):
        """ Gets the Races and Classes in a dungeon together as one json

        Args:
            data (str): Dungeon id of the dungeon

        Returns:
            List of all races and classes from one dungeon
        """
        try:
            char_config = [self.get_all_from_classes_as_json(data), self.get_all_from_races_as_json(data)]
            return char_config
        except IOError:
            pass

    def get_accesslist(self, dungeon_id):
        """ Gets an accesslist of a specific dungeon

        Args:
            dungeon_id (str): Dungeon id of the dungeon

        Returns:
            Accesslist of the dungeon
        """
        try:
            access_list = self.db_handler.get_access_list_by_dungeon_id_as_dict(dungeon_id)
            for entry in access_list:
                entry['isAllowed'] = bool(entry['isAllowed'])
            return access_list
        except IOError:
            pass

    def get_item_by_class_id(self, class_id: str):
        """ Gets an item via the class id

        Args:
            class_id (str): Id of the class which has an item

        Returns:
            Item object
        """
        item_data = self.db_handler.get_item_by_class_id(class_id)
        return Item(item_id=item_data['itemID'], name=item_data['itemName'], description=item_data['itemDescription'])
