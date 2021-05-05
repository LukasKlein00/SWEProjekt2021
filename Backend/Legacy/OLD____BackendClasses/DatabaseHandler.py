from mysql.connector import MySQLConnection

from BackendClasses.User import *
from BackendClasses.FullStackDungeon import *


class DatabaseHandler:
    def __init__(self, databasePath: MySQLConnection):
        self.databasePath = databasePath

    def registerUser(self, user: User):
        cursor = self.databasePath.cursor()
        query = """
            INSERT INTO mudcake.User
                    (user_id ,FirstName, LastName, user_name, password, email, isConfirmed)
                VALUES 
                    (%s, %s, %s, %s, %s, %s, %s) 
            """
        variables = (
            user.userID, user.firstName, user.lastName, user.username, user.password, user.eMail, user.confirmation
        )
        try:
            cursor.execute(query, variables)
            self.databasePath.commit()
        except IOError:
            pass

    def loginUser(self, user: User):
        cursor = self.databasePath.cursor()
        query = """
            SELECT user_name, user_id
            From mudcake.User
            WHERE (user_name = %s AND password = %s)
            """
        variables = (user.username, user.password)
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
                            WHERE (user_id = '{userID}' )
                            """
        cursor.execute(query)
        self.databasePath.commit()
        print("deleted")