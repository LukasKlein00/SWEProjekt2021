import mysql
from mysql.connector import MySQLConnection


class DatabaseHandler:
    """
    Class for handling Database transactions
    """
    def __init__(self):
        """
        constructor for DatabaseHandler
        """
        self.database_path = (mysql.connector.connect(
            host="193.196.53.67",
            port="1189",
            user="jack",
            password="123123"
        ))
        self.cursor = self.database_path.cursor()

    def register_user(self, user):
        """
        insert user to database after user registration
        :param user: a user object
        :return: nothing
        """
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
            self.cursor.execute(query, variables)
            self.database_path.commit()
        except IOError:
            pass

    def login_user(self, user):
        """
        checks if user is already in database, when client tries to login
        :param user: user object
        :return: returns the user from database if the user is exists in database
        """

        query = """
            SELECT UserName, UserID, isConfirmed
            From mudcake.User
            WHERE (UserName = %s AND Password = %s)
            """
        variables = (user.userName, user.password)
        self.cursor.execute(query, variables)
        try:
            query_data = self.cursor.fetchone()
            return query_data
        except IOError:
            return None

    def save_full_dungeon(self, dungeon):
        raise NotImplementedError

    def copy_dungeon(self, dungeon_id):
        '''
        copies a dungeon
        :param dungeon_id: id of dungeon
        '''
        # newDungeon = self.getFullDungeonByDungeonID(dungeonID)
        # get Dungeon by DungeonID and save with other ID!
        raise NotImplementedError

    def save_or_update_dungeon(self, dungeon):
        query = f"""
        INSERT INTO mudcake.Dungeon
            (DungeonID, DungeonName, DungeonDescription, MaxPlayers, DungeonMasterID, Private)
        VALUES 
            ("{dungeon.dungeonData.dungeon_id}", "{dungeon.dungeonData.name}", "{dungeon.dungeonData.description}", 
             "{dungeon.dungeonData.maxPlayers}", "{dungeon.dungeonData.dungeonMasterID}",
             "{int(dungeon.dungeonData.private)}") 
        ON DUPLICATE KEY UPDATE 
            DungeonID  = VALUES(DungeonID),
            DungeonName  = VALUES(DungeonName),
            DungeonDescription = VALUES(DungeonDescription),
            DungeonMasterID  = VALUES(DungeonMasterID),
            Private  = VALUES(Private)
                   """
        try:
            self.cursor.execute(query)
            dungeon.dungeonData.dungeonID = self.cursor.lastrowid
            self.database_path.commit()
            return dungeon.dungeonData.dungeonID

        except IOError:
            pass

    def get_everything(self, dungeon):
        raise NotImplementedError

    def get_user_by_id(self, user_id: int):
        raise NotImplementedError

    def get_user_id_by_email(self, email: str):
        '''
        reads the userid from the database belonging to the corresponding email
        :param email: email
        :return: returns the userid of the query 
        '''

        query = f"""
                    SELECT UserID
                    From mudcake.User
                    WHERE (Email = '{email}' )
                    """
        self.cursor.execute(query)
        try:
            query_data = self.cursor.fetchone()
            return query_data[0]
        except IOError:
            pass

    def get_character_by_id(self, character_id: int):
        raise NotImplementedError

    def get_dungeon_by_id(self, user_id: str):
        '''
        reads the dungeoninformation from the database belonging to the corresponding dungeonID
        :param dungeonID: id of the dungeon
        :return: value of query -> dungeonID, dungeonName, dungeonDescription 
        '''

        query = f"""
                    SELECT DungeonID, DungeonName, DungeonDescription
                    From mudcake.Dungeon
                    WHERE (DungeonMasterID = '{user_id}' )
                    """
        self.cursor.execute(query)
        try:
            query_data = self.cursor.fetchall()
            return query_data
        except IOError:
            pass

    def update_password_by_user_id(self, user_id: str, password: str):
        """
        Updates UserPassword in Database
        :param user_id: UserID
        :param password: UserPassword
        :return: true if transaction is successful
        """

        query = f"""
                        UPDATE mudcake.User
                        SET Password = '{password}'
                        WHERE UserID = '{user_id}'
                        """
        try:
            self.cursor.execute(query)
            self.database_path.commit()
            return True
        except IOError:
            return False

    def get_inventory_of_character(self, character):
        raise NotImplementedError

    def get_items_from_inventory(self):
        raise NotImplementedError

    def get_room_by_character_id(self, character):
        raise NotImplementedError

    def user_already_in_dungeon(self, character_id: int):
        raise NotImplementedError

    def write_game_state_to_database(self, dungeon):
        raise NotImplementedError

    def write_character_to_database(self, character):
        raise NotImplementedError

    def delete_dungeon_by_id(self, dungeon_id: str):
        '''
        deletes the dungeon that belongs to the given dungeonid
        :param dungeonID: id of the dungeon
        '''

        query = f"""
                            DELETE
                            From mudcake.Dungeon
                            WHERE (DungeonID = '{dungeon_id}' )
                            """
        try:
            self.cursor.execute(query)
            self.database_path.commit()
        except IOError:
            pass

    def delete_user_by_id(self, user_id):
        """
        deletes a user in database
        :param user_id: id of the user
        :return: true if transaction is successful
        """

        query = f"""
                            DELETE
                            From mudcake.User
                            WHERE (UserID = '{user_id}' )
                            """
        try:
            self.cursor.execute(query)
            self.database_path.commit()
            return True
        except IOError:
            return False

    def write_race_to_database(self, race, dungeon_id):
        '''
        insert a race object to database
        :param race: race object
        :param dungeon_id: id of dungeon 
        '''

        query = f"""
               INSERT INTO mudcake.Race
                   (DungeonID, RaceID, Name, Description)
               VALUES 
                   ("{dungeon_id}", "{race.race_id}", "{race.name}", "{race.description}")
                ON DUPLICATE KEY UPDATE
                DungeonID=VALUES(DungeonID), RaceID=VALUES(RaceID), Name=VALUES(Name), Description=VALUES(Description)
               """

        try:
            self.cursor.execute(query)
            self.database_path.commit()
        except IOError:
            pass

    def write_class_to_database(self, class_object, dungeon_id):
        '''
        insert a class object to database
        :param class_object: class object
        :param dungeon_id: id of dungeon 
        '''

        query = f"""
                      INSERT INTO mudcake.Class
                          (DungeonID, ClassID, Name, Description, ItemID)
                      VALUES 
                          (%s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    DungeonID = VALUES(DungeonID), ClassID=VALUES(ClassID), Name=VALUES(Name), 
                            Description=VALUES(Description), ItemID = VALUES(ItemID)
                      """
        variables = (dungeon_id, class_object.class_id, class_object.name, class_object.description, class_object.item_id)
        try:
            self.cursor.execute(query, variables)
            self.database_path.commit()
        except IOError:
            pass

    def write_room_to_database(self, room, dungeon_id):
        '''
        insert a room object to database
        :param room: room object
        :param dungeon_id: id of dungeon 
        '''

        print("cursor set")
        print(int(room.is_start_room))
        query = f"""
                             INSERT INTO mudcake.Room
                                 (DungeonID, RoomID, Name, Description, CoordinateX, CoordinateY, 
                                    North, East, South, West, isStartingRoom, NpcID, ItemID)
                             VALUES 
                                 (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                            ON DUPLICATE KEY UPDATE
                            DungeonID = VALUES(DungeonID), RoomID = VALUES(RoomID), Name = VALUES(Name), Description = VALUES(Description), CoordinateX = VALUES(CoordinateX), CoordinateY=VALUES(CoordinateY),
                            North=VALUES(North),East=VALUES(East),South=VALUES(South),West=VALUES(West),isStartingRoom=VALUES(isStartingRoom),NpcID=VALUES(NpcID),ItemID=VALUES(ItemID)
                             """
        variables = (
            dungeon_id, room.room_id, room.room_name, room.room_description, room.coordinate_x, room.coordinate_y,
            int(room.north), int(room.east), int(room.south), int(room.west), int(room.is_start_room), room.npc_id,
            room.item_id)
        print(query)
        print("Wrote room to database")
        try:
            self.cursor.execute(query, variables)
            self.database_path.commit()
        except IOError:
            print("aua")
            pass

    def change_registration_status(self, user_id: str):
        '''
        updates the isConfirmed field from False(0) to True(1)
        :param user_id: id of user
        :return: true if transaction was successful, false if not 
        '''

        query = f"""
                    UPDATE mudcake.User
                    SET isConfirmed = 1
                    WHERE (UserID = '{user_id}')
                    """
        try:
            print("Executing confirmation in database...")
            self.cursor.execute(query)
            self.database_path.commit()
            print("Executed")
            return True
        except IOError:
            return False

    def write_npc_to_database(self, npc, dungeon_id):
        '''
        insert a npc object to database
        :param npc: npc object
        :param dungeon_id: id of dungeon 
        '''

        query = f"""
                              INSERT INTO mudcake.Npc
                                  (DungeonID, NpcID, Name, Description, ItemID)
                              VALUES 
                                (%s,%s,%s,%s,%s)
                            ON DUPLICATE KEY UPDATE
                            DungeonID = VALUES(DungeonID), NpcID = VALUES(NpcID), Name = VALUES(Name), Description = VALUES(Description), ItemID = VALUES(ItemID)
    
                              """
        variables = (dungeon_id, npc.npc_id, npc.name, npc.description, npc.item)
        try:
            self.cursor.execute(query, variables)
            self.database_path.commit()
        except IOError:
            pass

    def write_item_to_database(self, item, dungeon_id):
        '''
        insert a item object to database
        :param item: item object
        :param dungeon_id: id of dungeon 
        '''

        query = f"""
                                      INSERT INTO mudcake.Item
                                          (DungeonID, ItemID, Name, Description)
                                      VALUES 
                                          (%s,%s,%s,%s)
                                    ON DUPLICATE KEY UPDATE 
                                    DungeonID = VALUES(DungeonID), ItemID = VALUES(ItemID), Name = VALUES(Name), Description =VALUES(Description)
                                      """
        variables = (dungeon_id, item.item_id, item.name, item.description)

        try:
            self.cursor.execute(query, variables)
            self.database_path.commit()
        except IOError:
            pass

    def get_character_by_dungeon_ID(self, dungeon_id: str):

        query = f"""
                    SELECT CharacterID, Lifepoints, Name, Description, ClassID, RaceID, UserID, DiscoverdMapID, RoomID
                    From mudcake.Character
                    WHERE (DungeonID = '{dungeon_id}')
                    """
        self.cursor.execute(query)
        try:
            query_data = self.cursor.fetchall()
            return query_data

        except IOError:
            pass

    def get_class_by_dungeon_id(self, dungeon_id: str):

        query = f"""
                    SELECT ClassID, Name, Description
                    From mudcake.Class
                    WHERE (DungeonID = '{dungeon_id}')
                    """
        self.cursor.execute(query)
        try:
            query_data = self.cursor.fetchall()
            return query_data
        except IOError:
            pass

    def get_race_by_dungeon_id(self, dungeon_id: str):

        query = f"""
                    SELECT RaceID, Name, Description
                    From mudcake.Race
                    WHERE (DungeonID = '{dungeon_id}')
                    """
        self.cursor.execute(query)
        try:
            query_data = self.cursor.fetchall()
            return query_data

        except IOError:
            pass

    def get_npc_by_dungeon_id(self, dungeon_id: str):

        query = f"""
                    SELECT NpcID, Name, Description, ItemID
                    From mudcake.Npc
                    WHERE (DungeonID = '{dungeon_id}')
                    """
        self.cursor.execute(query)
        try:
            query_data = self.cursor.fetchall()
            return query_data

        except IOError:
            pass

    def get_room_by_dungeon_id(self, dungeon_id: str):

        query = f"""
                    SELECT RoomID, Name, Description, CoordinateX, CoordinateY, North, East, South, West, 
                    isStartingRoom, NpcID, ItemID
                    From mudcake.Room
                    WHERE (DungeonID = '{dungeon_id}')
                    """
        self.cursor.execute(query)
        try:
            query_data = self.cursor.fetchall()
            return query_data

        except IOError:
            pass

    def get_item_by_dungeon_id(self, dungeon_id: str):

        query = f"""
                    SELECT ItemID, Name, Description
                    From mudcake.Item
                    WHERE (DungeonID = '{dungeon_id}')
                    """
        self.cursor.execute(query)
        try:
            query_data = self.cursor.fetchall()
            return query_data

        except IOError:
            pass

    def get_access_list_by_dungeon_id(self, dungeon_id: str):

        query = f"""
                    SELECT UserID, isAllowed
                    From mudcake.AccessList
                    WHERE (DungeonID = '{dungeon_id}')
                    """
        self.cursor.execute(query)
        try:
            query_data = self.cursor.fetchall()
            return query_data

        except IOError:
            pass

    def get_dungeon_data_by_dungeon_id(self, dungeon_id: str):

        query = f"""
                    SELECT DungeonID, DungeonMasterID, DungeonName, DungeonDescription, Private, MaxPlayers
                    From mudcake.Dungeon
                    WHERE (DungeonID = '{dungeon_id}')
                    """
        self.cursor.execute(query)
        try:
            query_data = self.cursor.fetchall()
            return query_data
        except IOError:
            pass

    def get_inventory_by_character_id(self, character_id: str):

        query = f"""
                    SELECT *
                    From mudcake.Inventory
                    WHERE (CharacterID = '{character_id}')
                    """
        self.cursor.execute(query)
        try:
            query_data = self.cursor.fetchone()
            return query_data
        except IOError:
            pass

    def check_user(self, user):
        """
        checks if user is already in database, when client is already logged in
        :param user: user object
        :return: returns true if credentials are still correct
        """

        query = f"""
            SELECT * 
            From mudcake.User
            WHERE (UserName = '{user.userName}' AND UserID = '{user.userID}' )
            """
        self.cursor.execute(query)
        try:
            query_data = self.cursor.fetchone()
            if query_data:
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

        query = f"""SELECT ItemTemplateID, Name, Description
            FROM mudcake.ItemTemplate
            WHERE (DungeonID = '{dungeon_id}')
            """
        try:
            self.cursor.execute(query)
            query_data = self.cursor.fetchall()
            return query_data
        except IOError:
            pass

    def get_npcs_by_dungeon_id(self, dungeon_id):

        query = f"""SELECT *
                    FROM mudcake.Npc
                    WHERE (DungeonID ) '{dungeon_id}"""
        try:
            query_data = self.cursor.execute(query)
            return query_data
        except IOError:
            pass

    def get_classes_by_dungeon_id(self, dungeon_id):

        query = f"""SELECT *
                    FROM mudcake.Class
                    WHERE (DungeonID ) '{dungeon_id}"""
        try:
            query_data = self.cursor.execute(query)
            return query_data
        except IOError:
            pass

    def get_rooms_by_dungeon_id(self, dungeon_id):

        query = f"""SELECT *
                    FROM mudcake.Room
                    WHERE (DungeonID ) '{dungeon_id}"""
        try:
            query_data = self.cursor.execute(query)
            return query_data
        except IOError:
            pass

    def get_races_by_dungeon_id(self, dungeon_id):

        query = f"""SELECT *
                    FROM mudcake.Race
                    WHERE (DungeonID ) '{dungeon_id}"""
        try:
            query_data = self.cursor.execute(query)
            return query_data
        except IOError:
            pass

    def user_status_on_access_list(self, user_id: str, dungeon_id: str):
        self.cursor.execute(f"""
                                    SELECT IsAllowed
                                    FROM mudcake.AccessList
                                    WHERE (DungeonID = %s AND UserID = %s )
                                    """, (user_id, dungeon_id))
        try:
            return self.cursor.fetchone()
        except IOError:
            print("Error occurred by accessing AccessList")
            raise IOError

    #################### NEW #######################

    def get_all_rooms_by_dungeon_id_old(self, dungeon_id: str):
        self.cursor.execute(f"""
                                    SELECT RoomID, isStartingRoom, Description, Name, CoordinateX, CoordinateY, North, East, South, West, NpcID, ItemID
                                    FROM mudcake.Room
                                    WHERE (DungeonID = '{dungeon_id}' )
                                    """)
        try:
            return self.cursor.fetchall()
        except IOError:
            print("Error occurred by accessing AccessList")
            raise IOError

    def get_all_rooms_by_dungeon_id(self, dungeon_id: str):
        dict_cursor = self.database_path.cursor(dictionary=True)
        dict_cursor.execute(f"""
                                    SELECT RoomID roomID,
                                           isStartingRoom isStartRoom,
                                           Description description,
                                           Name name, 
                                           CoordinateX x,
                                           CoordinateY y,
                                           North north,
                                           East east,
                                           South south,
                                           West west,
                                           NpcID npc,
                                           ItemID item
                                    FROM mudcake.Room
                                    WHERE (DungeonID = '{dungeon_id}' )
                                    """)
        try:
            temp = dict_cursor.fetchall()
            return temp
        except IOError:
            print("Error occurred by accessing AccessList")
            raise IOError

    def get_all_classes_by_dungeon_id(self, dungeon_id: str):
        dict_cursor = self.database_path.cursor(dictionary=True)
        dict_cursor.execute(f"""
                                    SELECT ClassID classID,
                                           Name name,
                                           Description description,
                                           ItemID equipment
                                    FROM mudcake.Class
                                    WHERE (DungeonID ='{dungeon_id}')
                                    """)
        try:
            return dict_cursor.fetchall()
        except IOError:
            print("Error occurred by accessing AccessList")
            raise IOError

    def get_all_races_by_dungeon_id(self, dungeon_id: str):
        dict_cursor = self.database_path.cursor(dictionary=True)
        dict_cursor.execute(f"""
                                    SELECT RaceID raceID,
                                           Name name,
                                           Description description,
                                           DungeonID dungeonID 
                                    FROM mudcake.Race
                                    WHERE (DungeonID = '{dungeon_id}' )
                                    """)
        try:
            return dict_cursor.fetchall()
        except IOError:
            print("Error occurred by accessing AccessList")
            raise IOError

    def get_all_item_by_dungeon_id(self, dungeon_id: str):
        dict_cursor = self.database_path.cursor(dictionary=True)
        dict_cursor.execute(f"""
                                    SELECT ItemID itemID,
                                           Description description,
                                           Name name
                                    FROM mudcake.Item
                                    WHERE (DungeonID = '{dungeon_id}')
                                    """)
        try:
            return dict_cursor.fetchall()
        except IOError:
            print("Error occurred by accessing AccessList")
            raise IOError

    def get_all_npc_by_dungeon_id(self, dungeon_id: str):
        dict_cursor = self.database_path.cursor(dictionary=True)
        dict_cursor.execute(f"""
                                    SELECT NpcID npcID,
                                           Name name,
                                           Description description,
                                           ItemID equipment       
                                    FROM mudcake.Npc
                                    WHERE (DungeonID = '{dungeon_id}')
                                    """)
        try:
            return dict_cursor.fetchall()
        except IOError:
            print("Error occurred by accessing AccessList")
            raise IOError

    def get_access_list_by_dungeon_ID(self, dungeon_id: str):
        dict_cursor = self.database_path.cursor(dictionary=True)
        dict_cursor.execute(f"""
                                    SELECT IsAllowed isAllowed,
                                           UserID userID)
                                    FROM mudcake.AccessList
                                    WHERE (DungeonID = '{dungeon_id}' )
                                    """,)
        try:
            return dict_cursor.fetchall()
        except IOError:
            print("Error occurred by accessing AccessList")
            raise IOError