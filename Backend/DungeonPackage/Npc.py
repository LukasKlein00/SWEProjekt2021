from DungeonPackage.Item import Item
from DatabaseHandler.DatabaseHandler import *


class Npc:
    def __init__(self, npc_id: str= None, dungeon_id: str= None, item: str = None, name: str = None, description: str = None ):
        self.npc_id = npc_id
        self.item = item
        self.name = name
        self.description = description
        self.dungeon_id = dungeon_id
        self.db_handler = DatabaseHandler()

    def load_data(self, dungeon_id: str):
        database_npc = self.db_handler.get_npc_by_dungeon_id(dungeon_id)
        self.npc_id = database_npc[0]
        self.name = database_npc[1]
        self.description = database_npc[2]
        self.dungeon_id = dungeon_id
        self.item = database_npc[4]
