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
        return

    def init_dungeon(self, dungeon_id: str):
        access_list = AccessList(dungeon_id)
