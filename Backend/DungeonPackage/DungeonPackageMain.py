from DungeonPackage.AccessList import AccessList
from DungeonPackage.ActiveDungeon import ActiveDungeon
from DungeonPackage.Character import Character
from DungeonPackage.DungeonData import DungeonData
from DungeonPackage.Room import Room


class DungeonPackageMain:
    def __init__(self, accessList: AccessList, activeDungeon: ActiveDungeon, character: Character,
                 dungeonData: DungeonData, room: Room):
        self.accessList = accessList
        self.activeDungeon = activeDungeon
        self.character = character
        self.dungeonData = dungeonData
        self.room = room
