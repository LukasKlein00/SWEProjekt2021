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

    def isDungeonMasterIn(self):
        raise NotImplementedError

    def addRoom(self):
        raise NotImplementedError

    def addItemToRoom(self):
        raise NotImplementedError

    def addNpcToRoom(self):
        raise NotImplementedError

    def loadData(self, dungeonID: str):
        databaseDungeonData = self.mDBHandler.get_dungeon_data_by_dungeon_ID(dungeonID)
        self.dungeon_id = databaseDungeonData[0]
        self.maxPlayers = databaseDungeonData[1]
        self.name = databaseDungeonData[2]
        self.description = databaseDungeonData[3]
        self.private = bool(databaseDungeonData[4])
        self.dungeonMasterID = databaseDungeonData[5]

    def isPrivate(self):
        raise NotImplementedError

    def overwriteDungeonMasterID(self):
        raise NotImplementedError

