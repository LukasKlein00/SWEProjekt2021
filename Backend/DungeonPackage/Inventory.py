from DatabaseHandler.DatabaseHandler import *


class Inventory:
    def __init__(self, inventoryID: str, characterID: int, ItemIDs: [int] = None):
        self.inventoryID = inventoryID
        self.characterID = characterID
        self.ItemIDs = ItemIDs
        self.mDBHandler = DatabaseHandler()

    def loadData(self, dungeonID: str):
        databaseInventory = self.mDBHandler.get_inventory_by_character_ID(dungeonID)
        self.inventoryID = databaseInventory[0]
        self.ItemIDs.append(databaseInventory[1])
        self.characterID = databaseInventory[2]
