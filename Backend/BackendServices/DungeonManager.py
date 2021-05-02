import uuid

import mysql

from DatabaseHandler.DatabaseHandler import DatabaseHandler
from DungeonPackage.ActiveDungeon import ActiveDungeon
from DungeonPackage.Class import Class
from DungeonPackage.DungeonData import DungeonData
from DungeonPackage.Item import Item
from DungeonPackage.Npc import Npc
from DungeonPackage.Race import Race
from DungeonPackage.Room import Room


class DungeonManager:
    def __init__(self, data=None):
        self.data = data


        self.mDBHandler = DatabaseHandler(mysql.connector.connect(
            host="193.196.53.67",
            port="1189",
            user="jack",
            password="123123"
        ))
        self.room_list = []
        self.race_list = []
        self.class_list = []
        self.item_list = []
        self.npc_list = []
        if data is not None:
            self.managed_dungeon = DungeonData(dungeonId=self.data['dungeonID'],
                                               dungeonMasterID=self.data['dungeonMasterID'],
                                               maxPlayers=self.data['maxPlayers'], name=self.data['dungeonName'],
                                               description=self.data['dungeonDescription'],
                                               private=self.data['private'],
                                               accessList=self.data['accessList'])
            self.check_for_dungeon_id()
            self.parse_config_data()

    def parse_config_data(self):
        # TODO: in allen Klassen den Default Wert von DungeonID entfernen, sobald die DungeonID vom Backend generierbar
        #  ist. IDs von Dungeondaten eventuell doch über autoincrement in Datenbank vornehmen.
        # accessList = AccessList()
        room_data = self.data['rooms']
        race_data = self.data['races']
        class_data = self.data['classes']
        items_data = self.data['items']
        npcs_data = self.data['npcs']

        # for dataForUser in data['accessList']:
        # accessList.addUserToAccessList(dataForUser['user'], dataForUser['isAllowed'])

        for room in room_data:
            print(room)
            new_room = Room(coordinate_x=room['x'], coordinate_y=room['y'], north=room['north'], east=room['east'],
                            south=room['south'], west=room['west'], room_id=str(uuid.uuid4()),
                            dungeon_id=self.managed_dungeon.dungeon_id)

            checkforname = 'name' in room
            if checkforname:
                new_room.room_name = room['name']
            else:
                new_room.room_name = None

            checkfordescription = 'description' in room
            if checkfordescription:
                new_room.room_description = room['description']
            else:
                new_room.room_description = "NULL"

            check_for_start_room = 'isStartRoom' in room
            if check_for_start_room:
                new_room.is_start_room = room['isStartRoom']
            else:
                new_room.is_start_room = False

            check_for_npc = 'npc' in room
            if check_for_npc:
                new_room.npc_id = room['Npc']
            else:
                new_room.npc_id = None

            check_for_item = 'item' in room
            if check_for_item:
                new_room.item_id = room['Item']
            else:
                new_room.item_id = None

            self.room_list.append(new_room)
            """room_list.append(
                Room(coordinate_x=room['x'], coordinate_y=room['y'], room_id=(str(uuid.uuid4())),
                     dungeon_id=data['dungeonID'],
                     room_description=room['description'], room_name=room['name'], is_start_room=room['isStartRoom'],
                     north=(bool(room['north'])), south=(bool(room['south'])), west=(bool(room['west'])),
                     east=bool((room['east']))))"""

        for race in race_data:
            print(race)
            new_race = Race(race_id=str(uuid.uuid4()), name=race['name'], description=race['description'],
                            dungeon_id=self.managed_dungeon.dungeon_id)
            self.race_list.append(new_race)

        for classes in class_data:
            print(classes)
            new_class = Class(class_id=str(uuid.uuid4()), name=classes['name'], description=classes['description'],
                              dungeon_id=self.managed_dungeon.dungeon_id)
            self.class_list.append(new_class)

        for item in items_data:
            print(item)
            new_item = Item(item_id=str(uuid.uuid4()), name=item['name'], description=item['description'])
            self.item_list.append(new_item)

        for npc in npcs_data:
            print(npc)
            new_npc = Npc(npc_id=str(uuid.uuid4()), name=npc['name'], item=npc['equipment'],
                          description=npc['description'], dungeon_id=self.managed_dungeon.dungeon_id)
            self.npc_list.append(new_npc)

    # dungeonData = DungeonData(dungeonId=(str(uuid.uuid4())), dungeonMasterID=data['dungeonMasterID'],
    # name=data['dungeonName'], description=data['dungeonDescription'],
    # maxPlayers=data['maxPlayers'], private=data['private'], accessList=accessList)
    # dungeon = ActiveDungeon(None, None, None, None, None, None, None, dungeonData=dungeonData)

    def write_dungeon_to_database(self):
        active_dungeon = ActiveDungeon(rooms=self.room_list, classes=self.class_list, npcs=self.npc_list,
                                       items=self.item_list, dungeonData=self.managed_dungeon, races=self.race_list,
                                       userIDs=None, characterIDs=None)  # Darf das None sein? :D
        try:
            self.mDBHandler.saveOrUpdateDungeon(active_dungeon)
            print("Dungeon saved")
            self._write_race_to_database()
            print("Races saved")
            self._write_class_to_database()
            print("Classes saved")
            print(self.room_list)
            self._write_rooms_to_database()
            print("Rooms saved")
            self._write_items_to_database()
            print("Items saved")
            self._write_npcs_to_database()
            print("Npcs saved")
            return self.managed_dungeon.dungeon_id
        except:
            pass

    def check_for_dungeon_id(self):
        if self.managed_dungeon.dungeon_id is None:
            self.managed_dungeon.dungeon_id = str(uuid.uuid4())

    def _write_race_to_database(self):
        print(self.race_list)
        for race in self.race_list:
            try:
                self.mDBHandler.write_race_to_database(race=race, dungeon_id=self.managed_dungeon.dungeon_id)
            except IOError:
                pass

    def _write_class_to_database(self):
        print(self.class_list)
        for classes in self.class_list:
            try:
                self.mDBHandler.write_class_to_database(class_object=classes,
                                                        dungeon_id=self.managed_dungeon.dungeon_id)
            except IOError:
                pass

    def _write_rooms_to_database(self):
        print(self.room_list)
        for room in self.room_list:
            try:
                self.mDBHandler.write_room_to_database(room=room, dungeon_id=self.managed_dungeon.dungeon_id)
            except IOError:
                pass

    def _write_items_to_database(self):
        print(self.item_list)
        for item in self.item_list:
            try:
                self.mDBHandler.write_item_to_database(item=item, dungeon_id=self.managed_dungeon.dungeon_id)
            except IOError:
                pass

    def _write_npcs_to_database(self):
        print(self.npc_list)
        for npc in self.npc_list:
            try:
                self.mDBHandler.write_npc_to_database(npc=npc, dungeon_id=self.managed_dungeon.dungeon_id)
            except IOError:
                pass

    def _loadDungeonFromDatabase(self):
        ######
        raise NotImplementedError

    def get_dungeon_by_id(self, user_id_data):
        return self.mDBHandler.get_dungeon_by_id(user_id_data)


    def delete_dungeon(self, dungeon_id):
        try:
            self.mDBHandler.delete_dungeon_by_id(dungeon_id)
        except IOError:
            pass

    def copy_dungeon(self, dungeon_id):
        self.room_list = []
        self.race_list = []
        self.class_list = []
        self.item_list = []
        self.npc_list = []
        try:
            items = self.mDBHandler.get_items_by_dungeon_id(dungeon_id)
            print(items)

        except IOError:
            pass

    def makeDungeonPrivate(self):
        raise NotImplementedError

    def makeDungeonPublic(self):
        raise NotImplementedError
