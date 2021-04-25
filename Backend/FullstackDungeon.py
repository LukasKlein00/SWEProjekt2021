import Backend.BackendClasses as backEnd


class FullStackDungeon:

    def __init__(self, dungeon: backEnd.Dungeon, rooms: backEnd.Room, character: backEnd.Character,
                 inventory: backEnd.Inventory):
        self.dungeon = dungeon
        self.rooms = rooms
        self.character = character
        self.inventory = inventory

    def move(self, userId: int, roomID: int, direction: backEnd.Directions):
        raise NotImplementedError

    def lookInRoom(self):
        raise NotImplementedError
