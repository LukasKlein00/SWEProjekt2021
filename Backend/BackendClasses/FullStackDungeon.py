from Backend.BackendClasses.Dungeon import *
from Backend.BackendClasses.Room import *
from Backend.BackendClasses.Character import *
from Backend.BackendClasses.Inventory import *
from Backend.BackendClasses.Directions import *

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
