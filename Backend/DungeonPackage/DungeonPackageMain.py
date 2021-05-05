from DungeonPackage.AccessList import AccessList
from DungeonPackage.ActiveDungeon import ActiveDungeon
from DungeonPackage.Character import Character
from DungeonPackage.DungeonData import DungeonData
from DungeonPackage.Room import Room


class DungeonPackageMain:
    def __init__(self, access_list: AccessList, active_dungeon: ActiveDungeon, character: Character,
                 dungeon_data: DungeonData, room: Room):
        self.access_list = access_list
        self.active_dungeon = active_dungeon
        self.character = character
        self.dungeon_data = dungeon_data
        self.room = room
