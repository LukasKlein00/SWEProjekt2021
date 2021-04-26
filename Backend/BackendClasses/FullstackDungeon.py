from BackendClasses.Directions import Directions
from BackendClasses.Dungeon import Dungeon
from BackendClasses.Room import Room
from BackendClasses.Character import Character
from BackendClasses.Inventory import Inventory


class FullStackDungeon:

    def __init__(self, dungeon: Dungeon, rooms: Room, character: Character, inventory: Inventory):
        self.dungeon = dungeon
        self.rooms = rooms

    def move(self, userId: int, roomID: int, direction: Directions):
        raise NotImplementedError

    def lookInRoom(self):
        raise NotImplementedError
