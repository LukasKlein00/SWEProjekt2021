from DatabaseHandler.DatabaseHandler import *


class Class:
    def __init__(self, class_id: str= None, name: str= None, description: str= None, dungeon_id: str= None, item_id: str = None):
        self.class_id = class_id
        self.name = name
        self.description = description
        self.dungeon_id = dungeon_id
        self.item_id = item_id
        self.mDBHandler = DatabaseHandler()

    def load_data(self, dungeon_id: str):
        database_class_data = self.mDBHandler.get_class_by_dungeon_id(dungeon_id)
        self.class_id = database_class_data[0]
        self.name = database_class_data[1]
        self.description = database_class_data[2]
        self.dungeon_id = database_class_data[3]
