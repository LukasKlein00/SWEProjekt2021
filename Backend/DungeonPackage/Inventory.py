from DungeonPackage.Item import *


class Inventory:
    def __init__(self, inventoryID: str, characterID: int, Items: [Item] = None):
        self.inventoryID = inventoryID
        self.characterID = characterID
        self.Items = Items
