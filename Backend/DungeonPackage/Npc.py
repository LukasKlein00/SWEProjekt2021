from DungeonPackage.Item import Item
from DatabaseHandler.DatabaseHandler import *


class Npc:
    def __init__(self, npc_id: str= None, dungeon_id: str= None, item: str = None, name: str = None, description: str = None ):
        self.npc_id = npc_id
        self.item = item
        self.name = name
        self.description = description
        self.dungeon_id = dungeon_id
        self.mDBHandler = DatabaseHandler()

    def loadData(self, dungeonID: str):
        databaseNpc = self.mDBHandler.get_npc_by_dungeon_ID(dungeonID)
        self.npc_id = databaseNpc[0]
        self.name = databaseNpc[1]
        self.description = databaseNpc[2]
        self.dungeon_id = dungeonID
        self.item = databaseNpc[4]
