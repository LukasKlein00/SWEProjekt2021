class Room:

    def __init__(self, coordinates: [int, int], roomID: int, dungeonID: int, roomDescription: str, roomName: str,
                 isStartRoom: bool, north: bool = True, south: bool = True, west: bool = True, east: bool = True,
                 userIDs: [int] = None, npcID: int = None, itemID: int = None):
        self.userIDs = userIDs
        self.coordinates = coordinates
        self.roomID = roomID
        self.dungeonID = dungeonID
        self.npcID = npcID
        self.itemID = itemID
        self.roomDescription = roomDescription
        self.roomName = roomName
        self.isStartRoom = isStartRoom
        self.north = north
        self.south = south
        self.west = west
        self.east = east
