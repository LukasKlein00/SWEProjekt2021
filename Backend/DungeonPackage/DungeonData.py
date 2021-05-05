from DungeonPackage.AccessList import AccessList as AccessList
from DatabaseHandler.DatabaseHandler import *


class DungeonData:
    def __init__(self, dungeonId: str = None, dungeonMasterID: str = None, maxPlayers: int = None, name: str = None,
                 description: str = None,
                 private: bool = False, accessList: AccessList = None):
        self.dungeon_id = dungeonId
        self.dungeonMasterID = dungeonMasterID
        self.maxPlayers = maxPlayers
        self.name = name
        self.description = description
        self.private = private
        self.accessList = accessList
        self.mDBHandler = DatabaseHandler()

    def is_dungeon_master_in(self):
        raise NotImplementedError

    def add_room(self):
        raise NotImplementedError

    def add_item_to_room(self):
        raise NotImplementedError

    def add_npc_to_room(self):
        raise NotImplementedError

    def load_data(self, dungeonID: str):
        databaseDungeonData = self.mDBHandler.get_dungeon_data_by_dungeon_ID(dungeonID)
        self.dungeon_id = databaseDungeonData[0]
        self.maxPlayers = databaseDungeonData[1]
        self.name = databaseDungeonData[2]
        self.description = databaseDungeonData[3]
        self.private = bool(databaseDungeonData[4])
        self.dungeonMasterID = databaseDungeonData[5]

    def is_private(self):
        raise NotImplementedError

    def overwrite_dungeon_master_id(self):
        raise NotImplementedError

