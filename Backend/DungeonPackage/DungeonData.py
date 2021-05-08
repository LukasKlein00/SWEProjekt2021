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
        print("DataRAW")
        for dataRaw in database_dungeon_data_raw:
            print(dataRaw)
        print("DATA")
        for data in database_dungeon_data:
            print(data)
        self.dungeon_id = database_dungeon_data[0]
        self.max_players = database_dungeon_data[5]
        self.name = database_dungeon_data[2]
        self.description = database_dungeon_data[3]
        self.private = bool(database_dungeon_data[4])
        self.dungeon_master_id = database_dungeon_data[1]

    def is_private(self):
        raise NotImplementedError

    def overwrite_dungeon_master_id(self):
        raise NotImplementedError

