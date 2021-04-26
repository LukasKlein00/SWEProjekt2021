from BackendClasses.Item import Item


class Inventory:
    def __init__(self, inventoryID: int, characterID: int, Items: [Item] = None):
        self.inventoryID = inventoryID
        self.characterID = characterID
        self.Items = Items
