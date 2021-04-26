class Dungeon:

    def __init__(self, dungeonID: int, classIDs: [int], maxPlayers: int, masterID: int, dungeonName: str,
                 dungeonDescription: str, private: bool, itemIDs: [int] = None, raceIDs: [int] = None,
                 npcIDs: [int] = None):
        self.dungeonID = dungeonID
        self.itemIDs = itemIDs
        self.raceIDs = raceIDs
        self.classIDs = classIDs
        self.maxPlayers = maxPlayers
        self.masterID = masterID
        self.npcIDs = npcIDs
        self.dungeonName = dungeonName
        self.dungeonDescription = dungeonDescription
        self.private = private

