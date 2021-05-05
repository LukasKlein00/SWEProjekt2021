from DatabaseHandler.DatabaseHandler import *


class AccessManager:
    def __init__(self):
        self.mDBHandler = DatabaseHandler()

    def __user_status_on_access_list(self, userID: str, dungeonID: str):
        ret = self.mDBHandler.user_status_on_access_list(userID, dungeonID)
        if ret != None:
            return bool(ret[0])
        else:
            return None

    def get_accesslist_for_dungeon(self):
        raise NotImplementetError

    def send_access_request_to_dm(self):
        raise NotImplementedError

    def join_user_to_white_list(self, userID: str, dungeonID: str):
        raise NotImplementedError

    def join_user_to_black_list(self, userID: str, dungeonID: str):
        raise NotImplementedError
