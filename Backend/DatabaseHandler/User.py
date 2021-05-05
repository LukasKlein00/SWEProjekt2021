class User:
    """
    User Class
    """
    def __init__(self, user_id: str = None, first_name: str = None, last_name: str = None, user_name: str = None,
                 e_mail: str = None, password: str = None, confirmation: bool = False):
        """
        constructor of user class
        """         
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = user_name
        self.e_mail = e_mail
        self.password = password
        self.confirmation = confirmation
