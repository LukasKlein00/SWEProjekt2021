from DatabaseHandler.DatabaseHandler import *


class Item:
    def __init__(self, item_id: str, name: str, description: str, dungeon_id: str = None):
        self.item_id = item_id
        self.name = name
        self.description = description
        self.dungeon_id = dungeon_id
        self.mDBHandler = DatabaseHandler()

    def loadData(self, dungeonID):
        databaseItem = self.mDBHandler.get_item_by_dungeon_ID(dungeonID)
        self.item_id = databaseItem[0]
        self.description = databaseItem[1]
        self.name = databaseItem[2]
