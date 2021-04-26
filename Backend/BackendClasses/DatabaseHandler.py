from mysql.connector import MySQLConnection

from BackendClasses.FullstackDungeon import FullStackDungeon
from BackendClasses.Character import Character
from BackendClasses.User import User
from BackendClasses.Inventory import Inventory
from BackendClasses.Dungeon import Dungeon


class DatabaseHandler:
    def __init__(self, databasePath: MySQLConnection):
        self.databasePath = databasePath

    def registerUser(self, user: User):
        cursor = self.databasePath.cursor()
        query = """
            INSERT INTO mudcake.User
                    (UserID ,FirstName, LastName, UserName, Password, Email, isConfirmed)
                VALUES 
                    (%s, %s, %s, %s, %s, %s, %s) 
            """
        variables = (
            user.userID, user.firstName, user.lastName, user.userName, user.password, user.eMail, user.confirmation
        )
        try:
            cursor.execute(query, variables)
            self.databasePath.commit()
        except IOError:
            pass

    def loginUser(self, user: User):
        cursor = self.databasePath.cursor()
        query = """
            SELECT UserName, UserID
            From mudcake.User
            WHERE (UserName = %s AND Password = %s)
            """
        variables = (user.userName, user.password)
        cursor.execute(query, variables)
        try:
            queryData = cursor.fetchone()
            return User(userID=queryData[1], userName=queryData[0])
        except:
            return None

    def getFullDungeonByDungeonID(self, dungeonID):
        raise NotImplementedError

    def saveFullDungeon(self, dungeon):
        raise NotImplementedError


    def copyDungeon(self, dungeonID):
        newDungeon = self.getFullDungeonByDungeonID(dungeonID)
        #DungeonID austragen und abspeichern!

    def saveOrUpdateDungeon(self, d: Dungeon):
        cursor = self.databasePath.cursor()
        query = """
        INSERT INTO mudcake.Dungeon
            (DungeonID, DungeonName, DungeonDescription, MaxPlayers, DungeonMasterID, Private)
        VALUES 
            (%s, %s, %s, %s, %s, %s) 
        ON DUPLICATE KEY UPDATE 
            DungeonID  = VALUES(DungeonID),
            DungeonName  = VALUES(DungeonName),
            DungeonDescription = VALUES(DungeonDescription),
            DungeonMasterID  = VALUES(DungeonMasterID),
            Private  = VALUES(Private)
                   """
        variables = (
            d.dungeonID, d.dungeonName, d.dungeonDescription, d.maxPlayers, d.dungeonMasterID, d.private
        )
        try:
            cursor.execute(query, variables)
            d.dungeonID = cursor.lastrowid
            self.databasePath.commit()
            return d.dungeonID

        except IOError:
            pass

    def getEverything(self, fullstackDungeon: FullStackDungeon):
        raise NotImplementedError

    def getUserByID(self, userID: int):
        raise NotImplementedError

    def getCharacterByID(self, characterID: int):
        raise NotImplementedError

    def getDungeonByID(self, dungeonID: int):
        cursor = self.databasePath.cursor()
        query = f"""
                    SELECT DungeonID, DungeonName, DungeonDescription
                    From mudcake.Dungeon
                    WHERE (DungeonMasterID = '{dungeonID}' )
                    """
        cursor.execute(query)
        try:
            queryData = cursor.fetchall()
            return queryData

        except:
            pass

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

    def deleteDungeonByID(self, dungeonID):
        cursor = self.databasePath.cursor()
        query = f"""
                            DELETE
                            From mudcake.Dungeon
                            WHERE (DungeonID = '{dungeonID}' )
                            """
        cursor.execute(query)
        self.databasePath.commit()

    def deleteUserByID(self, userID):
        cursor = self.databasePath.cursor()
        query = f"""
                            DELETE
                            From mudcake.User
                            WHERE (UserID = '{userID}' )
                            """
        cursor.execute(query)
        self.databasePath.commit()
        print("deleted")