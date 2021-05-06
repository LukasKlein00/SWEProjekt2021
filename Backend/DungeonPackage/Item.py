from DatabaseHandler.DatabaseHandler import *


class Item:
    def __init__(self, item_id: str= None, name: str= None, description: str= None, dungeon_id: str = None):
        self.item_id = item_id
        self.name = name
        self.description = description
        self.dungeon_id = dungeon_id
        self.db_handler = DatabaseHandler()

    def load_data(self, dungeonID):
        database_item = self.db_handler.get_item_by_dungeon_id(dungeonID)
        self.item_id = database_item[0]
        self.description = database_item[1]
        self.name = database_item[2]
