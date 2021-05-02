class AccessList:
    """
    class for handling access list
    """

    def __init__(self):
        """
        constructor for class AccessList
        """
        self.accessList = {"userID": [], "isAllowed": []}

    def addUserToAccessList(self, userID: str, isAllowed: bool):
        """
        adds a user to AccessList
        :param userID: id of user
        :param isAllowed: bool true=user on white list false=user on blacklist  
        """
        self.accessList["userID"].append(userID)
        self.accessList["isAllowed"].append(isAllowed)
