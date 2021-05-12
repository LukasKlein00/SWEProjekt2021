from DatabaseHandler.DatabaseHandler import DatabaseHandler


class AccessList:
    """
    class for handling access list
    """

    def __init__(self, dungeon_id: str = None):
        """
        constructor for class AccessList
        """
        self.access_list = []
        self.dungeon_id = dungeon_id

    def add_user_to_access_list(self, user_name: str, is_allowed: bool):
        """
        adds a user to AccessList
        :param user_id: id of user
        :param is_allowed: bool true=user on white list false=user on blacklist  
        """
        self.access_list.append({"user_name": user_name, "is_allowed":is_allowed})

    def load_data(self):
        """Part of the lazy loading process.
        Fills the AccessList class with data from the database.

        Returns:
            void: This Method only fills its own parameters
        """
        db_handler = DatabaseHandler()
        for user in db_handler.get_access_list_by_dungeon_id(self.dungeon_id):
            self.access_list.append({"user_name": user['userName'], "is_allowed": bool(user['isAllowed'])})
        return self