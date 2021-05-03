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
    """
    class for handling dungeon data
    """
    def __init__(self, data = None):
        """
        constructor for dungeon manager
        """
        self.data = data


        self.mDBHandler = DatabaseHandler()
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
        else:
            self.managed_dungeon = DungeonData()

    def parse_config_data(self):
        """
        deserializes the dungeon json and adds the deserialized elements to corresponding lists  
        """
        # TODO: in allen Klassen den Default Wert von DungeonID entfernen, sobald die DungeonID vom Backend generierbar
        #  ist. IDs von Dungeondaten eventuell doch über autoincrement in Datenbank vornehmen.
        # accessList = AccessList()

        race_data = self.data['races']
        items_data = self.data['items']
        npcs_data = self.data['npcs']
        room_data = self.data['rooms']
        class_data = self.data['classes']

        # for dataForUser in data['accessList']:
        # accessList.addUserToAccessList(dataForUser['user'], dataForUser['isAllowed'])

        for race in race_data:
            print(race)
            new_race = Race(race_id=str(uuid.uuid4()), name=race['name'], description=race['description'],
                            dungeon_id=self.managed_dungeon.dungeon_id)
            self.race_list.append(new_race)

        for item in items_data:
            print(item)
            new_item = Item(item_id=item['itemID'], name=item['name'], description=item['description'])
            self.item_list.append(new_item)

        for npc in npcs_data:
            print(npc)
            new_npc = Npc(npc_id=npc['npcID'], name=npc['name'],
                          description=npc['description'], dungeon_id=self.managed_dungeon.dungeon_id)

            if npc['equipment'] is None:
                new_npc.item = None
            else:
                new_npc.item = npc['equipment']['itemID']
                print(npc['equipment']['itemID'])
            self.npc_list.append(new_npc)

        for classes in class_data:
            print(classes)
            new_class = Class(class_id=str(uuid.uuid4()), name=classes['name'], description=classes['description'],
                              dungeon_id=self.managed_dungeon.dungeon_id)
            if npc['equipment'] is None:
                new_class.item = None
            else:
                new_class.item = classes['equipment']['itemID']
                print(classes['equipment']['itemID'])
            self.class_list.append(new_class)

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
                new_room.npc_id = room['npc']['npcID']
            else:
                new_room.npc_id = None

            check_for_item = 'item' in room
            if check_for_item:
                new_room.item_id = room['item']['itemID']
            else:
                new_room.item_id = None

            self.room_list.append(new_room)

    # dungeonData = DungeonData(dungeonId=(str(uuid.uuid4())), dungeonMasterID=data['dungeonMasterID'],
    # name=data['dungeonName'], description=data['dungeonDescription'],
    # maxPlayers=data['maxPlayers'], private=data['private'], accessList=accessList)
    # dungeon = ActiveDungeon(None, None, None, None, None, None, None, dungeonData=dungeonData)

    def write_dungeon_to_database(self):
        """
        writes whole Dungeon to Database
        """
        active_dungeon = ActiveDungeon(rooms=self.room_list, classes=self.class_list, npcs=self.npc_list,
                                       items=self.item_list, dungeonData=self.managed_dungeon, races=self.race_list,
                                       userIDs=None, characterIDs=None)  # Darf das None sein? :D
        try:
            self.mDBHandler.saveOrUpdateDungeon(active_dungeon)
            print("Dungeon saved")
           #for data in active_dungeon.races:
           #    print(data.name)
            self._write_races_to_database()
            print("Races saved")
            self._write_items_to_database()
            print("Items saved")
            self._write_classes_to_database()
            print("Classes saved")
            self._write_npcs_to_database()
            print("Npcs saved")
            print(self.room_list)
            self._write_rooms_to_database()
            print("Rooms saved")
            return self.managed_dungeon.dungeon_id
        except:
            pass

    def check_for_dungeon_id(self):
        """
        writes if Dungeon has an id already. if not, it creates one
        """
        if self.managed_dungeon.dungeon_id is None:
            self.managed_dungeon.dungeon_id = str(uuid.uuid4())

    def _write_races_to_database(self):
        """
        writes Races to Database
        """
        print(self.race_list)
        for race in self.race_list:
            try:
                self.mDBHandler.write_race_to_database(race=race, dungeon_id=self.managed_dungeon.dungeon_id)
            except IOError:
                pass

    def _write_classes_to_database(self):
        """
        writes Classes to Database
        """
        print(self.class_list)
        for classes in self.class_list:
            try:
                self.mDBHandler.write_class_to_database(class_object=classes,
                                                        dungeon_id=self.managed_dungeon.dungeon_id)
            except IOError:
                pass

    def _write_rooms_to_database(self):
        """
        writes Rooms to Database
        """
        print(self.room_list)
        for room in self.room_list:
            try:
                self.mDBHandler.write_room_to_database(room=room, dungeon_id=self.managed_dungeon.dungeon_id)
            except IOError:
                pass

    def _write_items_to_database(self):
        """
        writes Items to Database
        """
        print(self.item_list)
        for item in self.item_list:
            try:
                self.mDBHandler.write_item_to_database(item=item, dungeon_id=self.managed_dungeon.dungeon_id)
            except IOError:
                pass

    def _write_npcs_to_database(self):
        """
        writes Npcs to Database
        """
        print(self.npc_list)
        for npc in self.npc_list:
            try:
                self.mDBHandler.write_npc_to_database(npc=npc, dungeon_id=self.managed_dungeon.dungeon_id)
            except IOError:
                pass

    def deleteDungeonFromDatabase(self, dungeonID: str):
        self.mDBHandler.deleteDungeonByID(dungeonID)

    def _loadDungeonFromDatabase(self):
        ######
        raise NotImplementedError

    def get_dungeon_by_id(self, user_id_data):
        return self.mDBHandler.get_dungeon_by_id(user_id_data)

    def get_dungeon_data_by_dungeon_id(self, dungeon_id):
        return self.mDBHandler.get_dungeon_data_by_dungeon_id(dungeon_id)


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
            dungeon = self.mDBHandler.get_dungeon_data_by_dungeon_id(dungeon_id)
            print("Dungeon:")
            print(dungeon)
            self.managed_dungeon.dungeon_id = str(uuid.uuid4())
            self.managed_dungeon.dungeonMasterID = dungeon[1]
            self.managed_dungeon.name = dungeon[2] + " - copy"
            self.managed_dungeon.description = dungeon[3]
            self.managed_dungeon.private = dungeon[4]
            self.managed_dungeon.maxPlayers = dungeon[5]

            items = self.mDBHandler.get_item_by_dungeon_id(dungeon_id)
            for item in items:
                copied_item = Item(item_id=item[0], name=item[1], description=item[2], dungeon_id=self.managed_dungeon.dungeon_id)
                self.item_list.append(copied_item)

            print("Item List:")
            print(self.item_list)
            
            rooms = self.mDBHandler.get_room_by_dungeon_id(dungeon_id)
            for room in rooms:
                copied_room = Room(room_id=room[0], room_name=room[1], room_description=room[2], coordinate_x=room[3], coordinate_y=room[4], north=room[5], east=room[6], south=room[7], west=room[8], is_start_room=room[9], npc_id=room[10], item_id=room[11], dungeon_id=self.managed_dungeon.dungeon_id)
                self.room_list.append(copied_room)
            print("Room List:")
            print(self.room_list)

            races = self.mDBHandler.get_race_by_dungeon_id(dungeon_id)
            for race in races:
                copied_race = Race(race_id=race[0], name=race[1], description=race[2], dungeon_id=self.managed_dungeon.dungeon_id)
                self.race_list.append(copied_race)
            print("Race List:")
            print(self.race_list)

            classes = self.mDBHandler.get_class_by_dungeon_id(dungeon_id)
            for class_tuple in classes:
                copied_class = Class(class_id=class_tuple[0], name=class_tuple[1], description=class_tuple[2],dungeon_id=self.managed_dungeon.dungeon_id)
                self.class_list.append(copied_class)
            print("Class List:")
            print(self.class_list)

            npcs = self.mDBHandler.get_npc_by_dungeon_id(dungeon_id)
            for npc in npcs:
                copied_npc = Npc(npc_id=npc[0], name=npc[1], description=npc[2], item=npc[3], dungeon_id=self.managed_dungeon.dungeon_id)
                self.npc_list.append(copied_npc)
            print("NPC List:")
            print(self.npc_list)

            #TODO: AccessList
            self.write_dungeon_to_database()

        except IOError:
            pass

    def makeDungeonPrivate(self):
        raise NotImplementedError

    def makeDungeonPublic(self):
        raise NotImplementedError
