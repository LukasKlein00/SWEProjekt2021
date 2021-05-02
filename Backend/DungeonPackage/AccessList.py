from DatabaseHandler.DatabaseHandler import DatabaseHandler


class AccessList:

    def __init__(self, dungeonID):
        self.accessList = {"userID": [], "isAllowed": []}
        self.dungeonID = dungeonID
        self.mDBHandler = DatabaseHandler()

    def addUserToAccessList(self, userID: str, isAllowed: bool):
        self.accessList["userID"].append(userID)
        self.accessList["isAllowed"].append(isAllowed)

    def loadData(self):
        databaseAccessList = self.mDBHandler.get_access_list_by_dungeon_ID(self.dungeonID)
        self.accessList['userID'].append(databaseAccessList[2])
        self.accessList['isAllowed'].append(bool(databaseAccessList[1]))
