from DatabaseHandler.DatabaseHandler import *


class Inventory:
    def __init__(self, dungeon_id: str = None, user_id: str = None, inventory_id: str= None, item_ids: [int] = None):
        self.inventory_id = inventory_id
        self.dungeon_id = dungeon_id
        self.user_id = user_id
        self.item_ids = item_ids

    def load_data(self, dungeon_id: str, user_id: str):
        db_handler = DatabaseHandler()
        database_inventory = db_handler.get_inventory_by_dungeon_user_id(dungeon_id, user_id)
        self.inventory_id = database_inventory[0]
        self.item_ids.append(database_inventory[1])
        self.dungeon_id = dungeon_id
        self.user_id = user_id