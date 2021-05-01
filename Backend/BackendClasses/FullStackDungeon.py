from BackendClasses.Dungeon import *
from BackendClasses.Room import *
from BackendClasses.Character import *
from BackendClasses.Inventory import *
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
