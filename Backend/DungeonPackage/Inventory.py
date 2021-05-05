from DatabaseHandler.DatabaseHandler import *


class Inventory:
    def __init__(self, inventory_id: str= None, character_id: int= None, item_ids: [int] = None):
        self.inventory_id = inventory_id
        self.character_id = character_id
        self.item_ids = item_ids
        self.db_handler = DatabaseHandler()

    def load_data(self, dungeon_id: str):
        database_inventory = self.db_handler.get_inventory_by_character_id(dungeon_id)
        self.inventory_id = database_inventory[0]
        self.item_ids.append(database_inventory[1])
        self.character_id = database_inventory[2]
