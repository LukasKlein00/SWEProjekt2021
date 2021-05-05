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

    def add_user_to_access_list(self, userID: str, isAllowed: bool):
        """
        adds a user to AccessList
        :param userID: id of user
        :param isAllowed: bool true=user on white list false=user on blacklist  
        """
        self.accessList["userID"].append(userID)
        self.accessList["isAllowed"].append(isAllowed)

    def load_data(self):
        # TODO: Fix that shit
        databaseAccessList = self.mDBHandler.user_status_on_access_list(self.userID, self.dungeonID)
        self.accessList['userID'].append(databaseAccessList[2])
        self.accessList['isAllowed'].append(bool(databaseAccessList[1]))
