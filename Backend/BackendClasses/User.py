class User:
    def __init__(self, userID: int, firstName: str, lastName: str, userName: str, eMail: str, password: str, confirmation: bool):
        self.userID = userID
        self.firstName = firstName
        self.lastName = lastName
        self.userName = userName
        self.eMail = eMail
        self.password = password
        self.confirmation = confirmation