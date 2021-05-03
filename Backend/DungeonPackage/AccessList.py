from DatabaseHandler.DatabaseHandler import DatabaseHandler


class AccessList:
    """
    class for handling access list
    """

    def __init__(self, dungeonID):
        """
        constructor for class AccessList
        """
        self.accessList = {"userID": [], "isAllowed": []}
        self.dungeonID = dungeonID
        self.mDBHandler = DatabaseHandler()

    def addUserToAccessList(self, userID: str, isAllowed: bool):
        """
        adds a user to AccessList
        :param userID: id of user
        :param isAllowed: bool true=user on white list false=user on blacklist  
        """
        self.accessList["userID"].append(userID)
        self.accessList["isAllowed"].append(isAllowed)

    def loadData(self):
        databaseAccessList = self.mDBHandler.get_access_list_by_dungeon_ID(self.dungeonID)
        self.accessList['userID'].append(databaseAccessList[2])
        self.accessList['isAllowed'].append(bool(databaseAccessList[1]))
