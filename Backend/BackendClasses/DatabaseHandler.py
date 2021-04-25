from Backend.FullstackDungeon import FullStackDungeon
from Backend.BackendClasses.Character import Character
from Backend.BackendClasses.Inventory import Inventory

class DatabaseHandler:
    def __init__(self, databasePath:str):
        self.databasePath = databasePath

    def getEverything(self, fullstackDungeon: FullStackDungeon):
        raise NotImplementedError

    def getUserByID(self, userID: int):
        raise NotImplementedError

    def getCharacterByID(self, characterID: int):
        raise NotImplementedError

    def getDungeonByID(self, dungeonID: int):
        raise NotImplementedError

    def getInventarOfCharacter(self, character: Character):
        raise NotImplementedError

    def getItemsFromInventar(self, inventory: Inventory):
        raise NotImplementedError

    def getRoomByCharacterID(self, character: Character):
        raise NotImplementedError

    def userAlreadyInDungeon(self, characterID: int):
        raise NotImplementedError

    def writeGamestateToDatabase(self, dungeon: FullStackDungeon):
        raise NotImplementedError

    def writeCharacterToDatabase(self, character: Character):
        raise NotImplementedError