from DungeonPackage.Item import Item

class Npc:
    def __init__(self, npc_id: str, dungeon_id: str, item: Item = None, name: str = None, description: str = None ):
        self.npc_id = npc_id
        self.item = item
        self.name = name
        self.description = description
        self.dungeon_id = dungeon_id

