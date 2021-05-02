from mysql.connector import MySQLConnection

from DatabaseHandler.User import User
from DungeonPackage.ActiveDungeon import *
from DungeonPackage.Character import *
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
            SELECT UserName, UserID, isConfirmed
            From mudcake.User
            WHERE (UserName = %s AND Password = %s)
            """
        variables = (user.userName, user.password)
        cursor.execute(query, variables)
        try:
            queryData = cursor.fetchone()
            tempuser = User(userID=queryData[1], userName=queryData[0], confirmation=bool(queryData[2]))
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
        query = f"""
        INSERT INTO mudcake.Dungeon
            (DungeonID, DungeonName, DungeonDescription, MaxPlayers, DungeonMasterID, Private)
        VALUES 
            ("{dungeon.dungeonData.dungeon_id}", "{dungeon.dungeonData.name}", "{dungeon.dungeonData.description}", "{dungeon.dungeonData.maxPlayers}", "{dungeon.dungeonData.dungeonMasterID}", "{int(dungeon.dungeonData.private)}") 
        ON DUPLICATE KEY UPDATE 
            DungeonID  = VALUES(DungeonID),
            DungeonName  = VALUES(DungeonName),
            DungeonDescription = VALUES(DungeonDescription),
            DungeonMasterID  = VALUES(DungeonMasterID),
            Private  = VALUES(Private)
                   """
        """variables = (dungeon.dungeonData.dungeon_id, dungeon.dungeonData.name, dungeon.dungeonData.description,
                     dungeon.dungeonData.maxPlayers, dungeon.dungeonData.dungeonMasterID, dungeon.dungeonData.private)"""
        try:
            cursor.execute(query)
            dungeon.dungeonData.dungeonID = cursor.lastrowid
            self.databasePath.commit()
            return dungeon.dungeonData.dungeonID

        except IOError:
            pass

    def getEverything(self, dungeon: ActiveDungeon):
        raise NotImplementedError

    def getUserByID(self, userID: int):
        raise NotImplementedError

    def getUserIdByEmail(self, email: str):
        '''
        Placeholder
        '''
        cursor = self.databasePath.cursor()
        query = f"""
                    SELECT UserID
                    From mudcake.User
                    WHERE (Email = '{email}' )
                    """
        cursor.execute(query)
        try:
            queryData = cursor.fetchone()
            return queryData[0]
        except:
            pass

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

    def updatePasswordByUserID(self, userID: str, password: str):
        '''
        Updates UserPassword in Database
        :param userID: UserID
        :param password: UserPassword
        :return: true if transaction is succesfull
        '''
        cursor = self.databasePath.cursor()
        query = f"""
                        UPDATE mudcake.User
                        SET Password = '{password}'
                        WHERE UserID = '{userID}'
                        """
        try:
            cursor.execute(query)
            self.databasePath.commit()
            return True
        except:
            return False

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

    def write_race_to_database(self, race: Race, dungeon_id):
        cursor = self.databasePath.cursor()
        query = f"""
               INSERT INTO mudcake.Race
                   (DungeonID, RaceID, Name, Description)
               VALUES 
                   ("{dungeon_id}", "{race.race_id}", "{race.name}", "{race.description}")
               """

        try:
            cursor.execute(query)
            self.databasePath.commit()
        except IOError:
            pass

    def write_class_to_database(self, class_object: Class, dungeon_id):
        cursor = self.databasePath.cursor()
        query = f"""
                      INSERT INTO mudcake.Class
                          (DungeonID, ClassID, Name, Description)
                      VALUES 
                          ("{dungeon_id}", "{class_object.classID}", "{class_object.name}", "{class_object.description}")
                      """
        try:
            cursor.execute(query)
            self.databasePath.commit()
        except IOError:
            pass

    def write_room_to_database(self, room: Room, dungeon_id):
        cursor = self.databasePath.cursor()
        print("cursor set")
        print(int(room.is_start_room))
        query = f"""
                             INSERT INTO mudcake.Room
                                 (DungeonID, RoomID, Name, Description, CoordinateX, CoordinateY, 
                                    North, East, South, West, isStartingRoom, NpcID, ItemID)
                             VALUES 
                                 (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                             """
        variables = (
            dungeon_id, room.room_id, room.room_name, room.room_description, room.coordinate_x, room.coordinate_y,
            int(room.north), int(room.east), int(room.south), int(room.west), int(room.is_start_room), room.npc_id,
            room.item_id)
        print(query)
        print("Wrote room to database")
        try:
            cursor.execute(query, variables)
            self.databasePath.commit()
        except IOError:
            print("aua")
            pass

    # ("{dungeon_id}", "{room.room_id}", "{room.room_name}", "{room.room_description}","{room.coordinate_x}", "{room.coordinate_y}", "{int(room.north)}", "{int(room.east)}",  "{int(room.south)}", "{int(room.west)}", "{int(room.is_start_room)}","{room.npc_id}", "{room.item_id}")

    def change_registration_status(self, userID: str):
        cursor = self.databasePath.cursor()
        query = f"""
                    UPDATE mudcake.User
                    SET isConfirmed = 1
                    WHERE (UserID = '{userID}')
                    """
        try:
            print("Executing confirmation in database...")
            cursor.execute(query)
            self.databasePath.commit()
            print("Executed")
            return True
        except:
            return False

    def write_npc_to_database(self, npc: Npc, dungeon_id):
        cursor = self.databasePath.cursor()
        query = f"""
                              INSERT INTO mudcake.Npc
                                  (DungeonID, NpcID, Name, Description, ItemID)
                              VALUES 
                                (%s,%s,%s,%s,%s)
    
                              """
        variables= (dungeon_id, npc.npc_id, npc.name, npc.description, npc.item)
        #"{dungeon_id}", "{npc.npc_id}", "{npc.name}", "{npc.description}", "{npc.item}"
        try:
            cursor.execute(query, variables)
            self.databasePath.commit()
        except IOError:
            pass

    def write_item_to_database(self, item: Item, dungeon_id):
        cursor = self.databasePath.cursor()
        query = f"""
                                      INSERT INTO mudcake.ItemTemplate
                                          (DungeonID, ItemTemplateID, Name, Description)
                                      VALUES 
                                          (%s,%s,%s,%s)
                                      """
        variables = (dungeon_id, item.item_id, item.name, item.description)
        # "{dungeon_id}", "{item.item_id}", "{item.name}", "{item.description}"
        try:
            cursor.execute(query, variables)
            self.databasePath.commit()
        except IOError:
            pass
