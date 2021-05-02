import mysql
from mysql.connector import MySQLConnection


class DatabaseHandler:
    '''
    Class for handling Database transactions
    '''

    def __init__(self):
        '''
        constructor for DatabaseHandler
        :param databasePath: path to database
        '''
        self.databasePath = (mysql.connector.connect(
            host="193.196.53.67",
            port="1189",
            user="jack",
            password="123123"
        ))

    def registerUser(self, user):
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

    def loginUser(self, user):
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
            return queryData
        except IOError:
            return None

    def saveFullDungeon(self, dungeon):
        raise NotImplementedError

    def copy_dungeon(self, dungeonID):
        newDungeon = self.getFullDungeonByDungeonID(dungeonID)
        # DungeonID austragen und abspeichern!

    def saveOrUpdateDungeon(self, dungeon):
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
        try:
            cursor.execute(query)
            dungeon.dungeonData.dungeonID = cursor.lastrowid
            self.databasePath.commit()
            return dungeon.dungeonData.dungeonID

        except IOError:
            pass

    def getEverything(self, dungeon):
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

    def get_dungeon_by_id(self, user_id: str):
        cursor = self.databasePath.cursor()
        query = f"""
                    SELECT DungeonID, DungeonName, DungeonDescription
                    From mudcake.Dungeon
                    WHERE (DungeonMasterID = '{user_id}' )
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

    def getInventarOfCharacter(self, character):
        raise NotImplementedError

    def getItemsFromInventar(self):
        raise NotImplementedError

    def getRoomByCharacterID(self, character):
        raise NotImplementedError

    def userAlreadyInDungeon(self, characterID: int):
        raise NotImplementedError

    def writeGamestateToDatabase(self, dungeon):
        raise NotImplementedError

    def writeCharacterToDatabase(self, character):
        raise NotImplementedError

    def delete_dungeon_by_id(self, dungeon_id):

        cursor = self.databasePath.cursor()
        query = f"""
                            DELETE
                            From mudcake.Dungeon
                            WHERE (DungeonID = '{dungeon_id}' )
                            """
        try:
            cursor.execute(query)
            self.databasePath.commit()
        except IOError:
            pass

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

    def write_race_to_database(self, race, dungeon_id):
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

    def write_class_to_database(self, class_object, dungeon_id):
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

    def write_room_to_database(self, room, dungeon_id):
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

    def write_npc_to_database(self, npc, dungeon_id):
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

    def write_item_to_database(self, item, dungeon_id):
        cursor = self.databasePath.cursor()
        query = f"""
                                      INSERT INTO mudcake.ItemTemplate
                                          (DungeonID, ItemTemplateID, Name, Description)
                                      VALUES 
                                          (%s,%s,%s,%s)
                                      """
        variables = (dungeon_id, item.item_id, item.name, item.description)
        try:
            cursor.execute(query, variables)
            self.databasePath.commit()
        except IOError:
            pass

    def get_character_by_dungeon_ID(self, dungeonID: str):
        cursor = self.databasePath.cursor()
        query = f"""
                    SELECT *
                    From mudcake.Character
                    WHERE (dungeonID = '{dungeonID}')
                    """
        cursor.execute(query)
        try:
            queryData = cursor.fetchone()
            return queryData

        except IOError:
            pass

    def get_class_by_dungeon_ID(self, dungeonID: str):
        cursor = self.databasePath.cursor()
        query = f"""
                    SELECT *
                    From mudcake.Class
                    WHERE (dungeonID = '{dungeonID}')
                    """
        cursor.execute(query)
        try:
            queryData = cursor.fetchone()
            return queryData
        except IOError:
            pass

    def get_race_by_dungeon_ID(self, dungeonID: str):
        cursor = self.databasePath.cursor()
        query = f"""
                    SELECT *
                    From mudcake.Race
                    WHERE (dungeonID = '{dungeonID}')
                    """
        cursor.execute(query)
        try:
            queryData = cursor.fetchone()
            return queryData

        except IOError:
            pass

    def get_npc_by_dungeon_ID(self, dungeonID: str):
        cursor = self.databasePath.cursor()
        query = f"""
                    SELECT *
                    From mudcake.Npc
                    WHERE (dungeonID = '{dungeonID}')
                    """
        cursor.execute(query)
        try:
            queryData = cursor.fetchone()
            return queryData

        except IOError:
            pass

    def get_room_by_dungeon_ID(self, dungeonID: str):
        cursor = self.databasePath.cursor()
        query = f"""
                    SELECT *
                    From mudcake.Room
                    WHERE (dungeonID = '{dungeonID}')
                    """
        cursor.execute(query)
        try:
            queryData = cursor.fetchone()
            return queryData

        except IOError:
            pass

    def get_item_by_dungeon_ID(self, dungeonID: str):
        cursor = self.databasePath.cursor()
        query = f"""
                    SELECT *
                    From mudcake.Item
                    WHERE (dungeonID = '{dungeonID}')
                    """
        cursor.execute(query)
        try:
            queryData = cursor.fetchone()
            return queryData

        except IOError:
            pass

    def get_access_list_by_dungeon_ID(self, dungeonID: str):
        cursor = self.databasePath.cursor()
        query = f"""
                    SELECT *
                    From mudcake.AccessList
                    WHERE (dungeonID = '{dungeonID}')
                    """
        cursor.execute(query)
        try:
            queryData = cursor.fetchone()
            return queryData

        except IOError:
            pass

    def get_dungeon_data_by_dungeon_ID(self, dungeonID: str):
        cursor = self.databasePath.cursor()
        query = f"""
                    SELECT *
                    From mudcake.Dungeon
                    WHERE (dungeonID = '{dungeonID}')
                    """
        cursor.execute(query)
        try:
            queryData = cursor.fetchone()
            return queryData
        except IOError:
            pass

    def get_inventory_by_character_ID(self, characterID: str):
        cursor = self.databasePath.cursor()
        query = f"""
                    SELECT *
                    From mudcake.Inventory
                    WHERE (characterID = '{characterID}')
                    """
        cursor.execute(query)
        try:
            queryData = cursor.fetchone()
            return queryData
        except IOError:
            pass
    def checkUser(self, user: User):
        '''
        checks if user is already in database, when client is already logged in
        :param user: user object
        :return: returns true if credentials are still correct
        '''
        cursor = self.databasePath.cursor()
        query = f"""
            SELECT * 
            From mudcake.User
            WHERE (UserName = '{user.userName}' AND UserID = '{user.userID}' )
            """
        cursor.execute(query)
        try:
            queryData = cursor.fetchone()
            if queryData:
                return True
            else:
                return False
        except IOError:
            return False

    def get_items_by_dungeon_id(self, dungeon_id):
        """

        :param dungeon_id:
        :type dungeon_id:
        :return:
        :rtype:
        """
        cursor = self.databasePath.cursor()
        query=f"""SELECT ItemTemplateID, Name, Description
            FROM mudcake.ItemTemplate
            WHERE (DungeonID = '{dungeon_id}')
            """
        try:
            cursor.execute(query)
            query_data = cursor.fetchall()
            return query_data
        except IOError:
            pass

    def get_npcs_by_dungeon_id(self, dungeon_id):
        cursor = self.databasePath.cursor()
        query = f"""SELECT *
                    FROM mudcake.Npc
                    WHERE (DungeonID ) '{dungeon_id}"""
        try:
            query_data = cursor.execute(query)
            return query_data
        except IOError:
            pass
    def get_classes_by_dungeon_id(self, dungeon_id):
        cursor = self.databasePath.cursor()
        query = f"""SELECT *
                    FROM mudcake.Class
                    WHERE (DungeonID ) '{dungeon_id}"""
        try:
            query_data = cursor.execute(query)
            return query_data
        except IOError:
            pass

    def get_rooms_by_dungeon_id(self, dungeon_id):
        cursor = self.databasePath.cursor()
        query = f"""SELECT *
                    FROM mudcake.Room
                    WHERE (DungeonID ) '{dungeon_id}"""
        try:
            query_data = cursor.execute(query)
            return query_data
        except IOError:
            pass
    def get_races_by_dungeon_id(self, dungeon_id):
        cursor = self.databasePath.cursor()
        query = f"""SELECT *
                    FROM mudcake.Race
                    WHERE (DungeonID ) '{dungeon_id}"""
        try:
            query_data = cursor.execute(query)
            return query_data
        except IOError:
            pass
