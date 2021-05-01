from mysql.connector import MySQLConnection

from DatabaseHandler.User import User
from DungeonPackage.ActiveDungeon import *
from DungeonPackage.Character import   *
from DungeonPackage.Inventory import *


class DatabaseHandler:
    '''
    Class for handling Database transactions
    '''
    def __init__(self, databasePath: MySQLConnection):
        '''
        constructor for DatabaseHandler
        :param databasePath: path to database
        '''
        self.databasePath = databasePath

    def registerUser(self, user: User):
        '''
        insert user to database after user registration
        :param user: a user object
        :return: nothing
        '''
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
        '''
        checks if user is already in database, when client tries to login
        :param user: user object
        :return: returns the user from database if the user is exists in database
        '''
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
            tempuser = User(userID=queryData[1], userName=queryData[0])
            return tempuser
        except IOError:
            return None

    def getFullDungeonByDungeonID(self, dungeonID):
        raise NotImplementedError

    def saveFullDungeon(self, dungeon):
        raise NotImplementedError

    def copyDungeon(self, dungeonID):
        newDungeon = self.getFullDungeonByDungeonID(dungeonID)
        # DungeonID austragen und abspeichern!

    def saveOrUpdateDungeon(self, dungeon: ActiveDungeon):
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
            dungeon.dungeonData.dungeonId, dungeon.dungeonData.name, dungeon.dungeonData.description,
            dungeon.dungeonData.maxPlayers, dungeon.dungeonData.dungeonMasterID, dungeon.dungeonData.private
        )
        try:
            cursor.execute(query, variables)
            dungeon.dungeonData.dungeonID = cursor.lastrowid
            self.databasePath.commit()
            return dungeon.dungeonData.dungeonID

        except IOError:
            pass

    def getEverything(self, dungeon: ActiveDungeon):
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

    def writeGamestateToDatabase(self, dungeon: ActiveDungeon):
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
        '''
        deletes a user in database
        :param userID: id of the user
        :return: true if transaction is successful
        '''
        cursor = self.databasePath.cursor()
        query = f"""
                            DELETE
                            From mudcake.User
                            WHERE (UserID = '{userID}' )
                            """
        try:
            cursor.execute(query)
            self.databasePath.commit()
            return True
        except:
            return False

