from DatabaseHandler.DatabaseHandler import DatabaseHandler


class AccessList:
    """
    class for handling access list
    """

    def __init__(self, dungeon_id):
        """
        constructor for class AccessList
        """
        self.access_list = {"user_id": [], "isAllowed": []}
        self.dungeon_id = dungeon_id
        self.db_handler = DatabaseHandler()

    def add_user_to_access_list(self, user_id: str, is_allowed: bool):
        """
        adds a user to AccessList
        :param user_id: id of user
        :param is_allowed: bool true=user on white list false=user on blacklist  
        """
        self.access_list["user_id"].append(user_id)
        self.access_list["isAllowed"].append(is_allowed)

    def load_data(self):
        # TODO: Fix that shit
        database_access_list = self.db_handler.user_status_on_access_list(self.userID, self.dungeon_id)
        self.access_list['user_id'].append(database_access_list[2])
        self.access_list['isAllowed'].append(bool(database_access_list[1]))
