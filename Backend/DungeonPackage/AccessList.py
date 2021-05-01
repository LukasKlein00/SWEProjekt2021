class AccessList:

    def __init__(self):
        self.accessList = {"userID": [], "isAllowed": []}

    def addUserToAccessList(self, userID: str, isAllowed: bool):
        self.accessList["userID"].append(userID)
        self.accessList["isAllowed"].append(isAllowed)
