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

    def add_item(self, item: Item):
        """
        adds an item to activeDungeon
        :param item: item object
        """
        self.items.append(item)

    def add_race(self, race: Race):
        """
        adds an race to activeDungeon
        :param race: race object
        """
        self.races.append(race)

    def is_dungeon_master_in_game(self) -> bool:
        """
        checks if dungeon master is in game
        :param item: item object
        :return: True if so
        """
        return self.userIDs.contains(self.dungeonData.dungeonMasterID)

    def add_room(self, room: Room):
        """
        adds an room to activeDungeon
        :param room: room object
        """
        self.rooms.append(room)

    def add_class(self, dClass: Class):
        """
        adds an class to activeDungeon
        :param item: item object
        """
        self.classes.append(dClass)

    def load_data(self):
        raise NotImplementedError

    def change_race_visibility(self):
        raise NotImplementedError

    def change_class_visibility(self):
        raise NotImplementedError

    def move_character(self):
        raise NotImplementedError
