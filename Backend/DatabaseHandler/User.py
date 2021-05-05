class User:
    """
    User Class
    """
    def __init__(self, userID: str = None, firstName: str = None, lastName: str = None, userName: str = None,
                 eMail: str = None, password: str = None, confirmation: bool = False):
        """
        constructor of user class
        """         
        self.userID = userID
        self.firstName = firstName
        self.lastName = lastName
        self.username = userName
        self.eMail = eMail
        self.password = password
        self.confirmation = confirmation
