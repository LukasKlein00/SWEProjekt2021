from DungeonPackage.ActiveDungeon import ActiveDungeon
from DungeonPackage.Class import Class
from DungeonPackage.DungeonData import DungeonData
from DungeonPackage.Item import Item
from DungeonPackage.Npc import Npc
from DungeonPackage.Race import Race
from DungeonPackage.Room import Room
from DungeonPackage.AccessList import AccessList

class ActiveDungeonHandler:
    def __init__(self):
        self.active_active_dungeon_ids = []
        self.active_active_dungeons = []

    def init_dungeon(self, dungeon_id: str):
        access_list_object = AccessList(dungeon_id).load_data()
        active_dungeon_object = ActiveDungeon()

    def dungeon_join(self, dungeon_id):
        self.active_active_dungeon_ids.append(dungeon_id)
        self.active_active_dungeons.append(self.init_dungeon(dungeon_id))
