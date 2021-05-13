from DatabaseHandler.DatabaseHandler import *


class AccessManager:
    def __init__(self):
        self.db_handler = DatabaseHandler()

    def user_status_on_access_list(self, dungeon_id: str, user_name: str):
        ret = self.db_handler.user_status_on_access_list(user_name, dungeon_id)
        print("ret is ne rat ", ret)
        return bool(ret[0]) if ret else None
      #if ret:
      #    ret_zerro = bool(ret[0])
      #    return ret_zerro
      #else:
      #    return None

    def get_accesslist_for_dungeon(self):
        raise NotImplementedError

    def send_access_request_to_dm(self):
        raise NotImplementedError

    def join_user_to_white_list(self, user_id: str, dungeon_id: str):
        raise NotImplementedError

    def join_user_to_black_list(self, user_id: str, dungeon_id: str):
        raise NotImplementedError
