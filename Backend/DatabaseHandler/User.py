class User:
    """
    User Class
    """
    def __init__(self, user_id: str = None, first_name: str = None, last_name: str = None, user_name: str = None,
                 e_mail: str = None, password: str = None, confirmation: bool = False):
        """
        constructor of user class
        """         
        self.userID = user_id
        self.firstName = first_name
        self.lastName = last_name
        self.userName = user_name
        self.eMail = e_mail
        self.password = password
        self.confirmation = confirmation
