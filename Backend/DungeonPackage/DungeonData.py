from DungeonPackage.AccessList import AccessList as AccessList


class DungeonData:
    def __init__(self, dungeonId: int, dungeonMasterID: int, maxPlayers: int, name: str, description: str,
                 private: bool, accessList: AccessList):
        self.dungeonId = dungeonId
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
