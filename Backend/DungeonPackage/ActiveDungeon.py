from DungeonPackage.Class import Class as Class
from DungeonPackage.DungeonData import DungeonData as DungeonData
from DungeonPackage.Item import Item as Item
from DungeonPackage.Npc import Npc as Npc
from DungeonPackage.Race import Race as Race
from DungeonPackage.Room import Room as Room


class ActiveDungeon:
    """
    class for handling active dungeons
    """
    def __init__(self, userIDs: [int] = None, characterIDs: [int] = None, rooms: [Room] = None, npcs: [Npc] = None,
                 items: [Item] = None, races: [Race] = None,
                 classes: [Class] = None, dungeonData: DungeonData = None):
        """
        constructor for ActiveDungeon class
        """
        self.userIDs = userIDs
        self.characterIDs = characterIDs
        self.rooms = rooms
        self.npcs = npcs
        self.items = items
        self.races = races
        self.classes = classes
        self.dungeonData = dungeonData

    def addItem(self, item: Item):
        """
        adds an item to activeDungeon
        :param item: item object
        """
        self.items.append(item)

    def addRace(self, race: Race):
        """
        adds an race to activeDungeon
        :param race: race object
        """
        self.races.append(race)

    def isDungeonMasterInGame(self) -> bool:
        """
        checks if dungeon master is in game
        :param item: item object
        :return: True if so
        """
        return self.userIDs.contains(self.dungeonData.dungeonMasterID)

    def addRoom(self, room: Room):
        """
        adds an room to activeDungeon
        :param room: room object
        """
        self.rooms.append(room)

    def addClass(self, dClass: Class):
        """
        adds an class to activeDungeon
        :param item: item object
        """
        self.classes.append(dClass)

    def loadData(self):
        raise NotImplementedError

    def changeRaceVisibility(self):
        raise NotImplementedError

    def changeClassVisibility(self):
        raise NotImplementedError

    def moveCharacter(self):
        raise NotImplementedError
