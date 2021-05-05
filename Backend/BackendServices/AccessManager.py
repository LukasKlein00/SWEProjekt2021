from DatabaseHandler.DatabaseHandler import *


class AccessManager:
    def __init__(self):
        self.mDBHandler = DatabaseHandler()

    def __user_status_on_access_list(self, user_id: str, dungeon_id: str):
        ret = self.mDBHandler.user_status_on_access_list(user_id, dungeon_id)
        if ret != None:
            return bool(ret[0])
        else:
            return None

    def get_accesslist_for_dungeon(self):
        raise NotImplementedError

    def send_access_request_to_dm(self):
        raise NotImplementedError

    def join_user_to_white_list(self, user_id: str, dungeon_id: str):
        raise NotImplementedError

    def join_user_to_black_list(self, user_id: str, dungeon_id: str):
        raise NotImplementedError
