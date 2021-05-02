from DatabaseHandler.DatabaseHandler import *
from DungeonPackage.Inventory import *


class Character:
    def __init__(self, characterID: str, lifePoints: int, name: str, description: str, classID: int, raceID: int,
                 userID: str, discoveredMapID: int, inventory: Inventory = None):
        self.characterID = characterID
        self.lifePoints = lifePoints
        self.name = name
        self.description = description
        self.classID = classID
        self.raceID = raceID
        self.userID = userID
        self.discoveredMap = discoveredMapID
        self.inventory = inventory
        self.mDBHandler = DatabaseHandler()

    def loadData(self, dungeonID: str):
        databaseCharacterData = self.mDBHandler.get_character_by_dungeon_ID(dungeonID)
        self.characterID = databaseCharacterData[0]
        self.lifePoints = databaseCharacterData[1]
        self.name = databaseCharacterData[2]
        self.description = databaseCharacterData[3]
        self.classID = databaseCharacterData[4]
        self.raceID = databaseCharacterData[5]
        self.userID = databaseCharacterData[6]
        self.discoveredMap = databaseCharacterData[7]
