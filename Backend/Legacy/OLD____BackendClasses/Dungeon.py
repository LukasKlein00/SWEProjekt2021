class Dungeon:

    def __init__(self, dungeonID: int, dungeonMasterID: str, maxPlayers: int, dungeonName: str, dungeonDescription: str, private: bool):
        self.dungeonID = dungeonID
        self.dungeonMasterID = dungeonMasterID
        self.maxPlayers = maxPlayers
        self.dungeonName = dungeonName
        self.dungeonDescription = dungeonDescription
        self.private = private

