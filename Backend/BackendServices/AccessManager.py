from DatabaseHandler.DatabaseHandler import *


class AccessManager:
    def __init__(self):
        self.db_handler = DatabaseHandler()
#todo: lukas!
    def user_status_on_access_list(self, user_id: str, dungeon_id: str, user_name: str):
        ret = self.db_handler.user_status_on_access_list(user_name, dungeon_id)
        return bool(ret[0]) if ret != None else False

    def get_accesslist_for_dungeon(self):
        raise NotImplementedError

    def send_access_request_to_dm(self):
        raise NotImplementedError

    def join_user_to_white_list(self, user_id: str, dungeon_id: str):
        raise NotImplementedError

    def join_user_to_black_list(self, user_id: str, dungeon_id: str):
        raise NotImplementedError
