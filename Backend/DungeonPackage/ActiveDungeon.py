from DungeonPackage.Room import Room as Room
from DungeonPackage.Npc import Npc as Npc
from DungeonPackage.Item import Item as Item
from DungeonPackage.Race import Race as Race
from DungeonPackage.Class import Class as Class
from DungeonPackage.DungeonData import DungeonData as DungeonData


class ActiveDungeon:
    def __init__(self, userIDs: [int], characterIDs: [int], rooms: [Room], npcs: [Npc], items: [Item], races: [Race],
                 classes: [Class], dungeonData: DungeonData):
        self.userIDs = userIDs
        self.characterIDs = characterIDs
        self.rooms = rooms
        self.npcs = npcs
        self.items = items
        self.races = races
        self.classes = classes
        self.dungeonData = dungeonData

    def addItem(self, item: Item):
        self.items.append(item)

    def addRace(self, race: Race):
        self.races.append(race)

    def isDungeonMasterInGame(self) -> bool:
        return self.userIDs.contains(self.dungeonData.dungeonMasterID)

    def addRoom(self, room: Room):
        self.rooms.append(room)

    def addClass(self, dClass: Class):
        self.classes.append(dClass)

    def loadData(self):
        raise NotImplementedError

    def changeRaceVisibility(self):
        raise NotImplementedError

    def changeClassVisibility(self):
        raise NotImplementedError

    def moveCharacter(self):
        raise NotImplementedError
