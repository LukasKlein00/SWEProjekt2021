from Backend.BackendClasses.Directions import Directions
from Backend.BackendClasses.Dungeon import Dungeon
from Backend.BackendClasses.Room import Room
from Backend.BackendClasses.Character import Character
from Backend.BackendClasses.Inventory import Inventory


class FullStackDungeon:

    def __init__(self, dungeon: Dungeon, rooms: Room, character: Character, inventory: Inventory):
        self.dungeon = dungeon
        self.rooms = rooms

    def move(self, userId: int, roomID: int, direction: Directions):
        raise NotImplementedError

    def lookInRoom(self):
        raise NotImplementedError
