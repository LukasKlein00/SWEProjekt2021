from DatabaseHandler.DatabaseHandler import DatabaseHandler


class AccessList:
    """
    class for handling access list
    """

    def __init__(self, dungeonID):
        """
        constructor for class AccessList
        """
        self.accessList = {"user_id": [], "isAllowed": []}
        self.dungeonID = dungeonID
        self.mDBHandler = DatabaseHandler()

    def add_user_to_access_list(self, userID: str, isAllowed: bool):
        """
        adds a user to AccessList
        :param userID: id of user
        :param isAllowed: bool true=user on white list false=user on blacklist  
        """
        self.accessList["user_id"].append(userID)
        self.accessList["isAllowed"].append(isAllowed)

    def load_data(self):
        # TODO: Fix that shit
        databaseAccessList = self.mDBHandler.user_status_on_access_list(self.userID, self.dungeonID)
        self.accessList['user_id'].append(databaseAccessList[2])
        self.accessList['isAllowed'].append(bool(databaseAccessList[1]))
