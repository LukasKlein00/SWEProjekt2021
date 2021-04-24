class Room:

    def __init__(self, userIDs: [int], coordinates: [int, int], roomID: int, dungeonID: int, npcID: int, itemID: int,
                 roomDescription: str, roomName: str, isStartRoom: bool, north: bool, south: bool, west: bool,
                 east: bool):
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
