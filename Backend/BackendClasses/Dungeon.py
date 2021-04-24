class Dungeon:

    def __init__(self, dungeonID: int, itemIDs: [int], raceIDs: [int], classIDs: [int], maxPlayers: int,
                 userIDs: [int], npcIDs: [int], dungeonName: str, dungeonDescription: str, private: bool):
        self.dungeonID = dungeonID
        self.itemIDs = itemIDs
        self.raceIDs = raceIDs
        self.classIDs = classIDs
        self.maxPlayers = maxPlayers
        self.userIDs = userIDs
        self.npcIDs = npcIDs
        self.dungeonName = dungeonName
        self.dungeonDescription = dungeonDescription
        self.private = private
