from BackendClasses.Dungeon import *
from DungeonPackage.Room import *
from DungeonPackage.Character import *
from DungeonPackage.Inventory import *
from BackendClasses.Directions import *


class FullStackDungeon:

    def __init__(self, dungeon: Dungeon, rooms: Room, character: Character,
                 inventory: Inventory):
        self.dungeon = dungeon
        self.rooms = rooms
        self.character = character
        self.inventory = inventory

    def move(self, userId: int, roomID: int, direction: Directions):
        raise NotImplementedError

    def lookInRoom(self):
        raise NotImplementedError