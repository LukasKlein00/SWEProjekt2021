from DatabaseHandler.DatabaseHandler import *


class Race:

    def __init__(self, race_id: str, name: str, description: str, dungeon_id: str):
        self.race_id = race_id
        self.name = name
        self.description = description
        self.dungeon_id = dungeon_id
        self.mDBHandler = DatabaseHandler()

    def loadData(self, dungeonID: str):
        databaseRace = self.mDBHandler.get_race_by_dungeon_ID(dungeonID)
        self.race_id = databaseRace[0]
        self.name = databaseRace[1]
        self.description = databaseRace[2]
        self.dungeon_id = dungeonID
