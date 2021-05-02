from DungeonPackage.AccessList import AccessList as AccessList


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

    def isDungeonMasterIn(self):
        raise NotImplementedError

    def addRoom(self):
        raise NotImplementedError

    def addItemToRoom(self):
        raise NotImplementedError

    def addNpcToRoom(self):
        raise NotImplementedError

    def loadData(self):
        raise NotImplementedError

    def isPrivate(self):
        raise NotImplementedError

    def overwriteDungeonMasterID(self):
        raise NotImplementedError
