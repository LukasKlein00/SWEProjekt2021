class User:
    def __init__(self, userID: str = None, firstName: str = None, lastName: str = None, userName: str = None,
                 eMail: str = None, password: str = None, confirmation: bool = False):
        self.userID = userID
        self.firstName = firstName
        self.lastName = lastName
        self.userName = userName
        self.eMail = eMail
        self.password = password
        self.confirmation = confirmation
