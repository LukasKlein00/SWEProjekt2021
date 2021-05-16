#!/usr/bin/env python
__author__ = "Jan Gruchott"
__copyright__ = "Copyright 2021, The MUDCake Project"
__credits__ = "Hauke Presig, Jack Drillisch, Jan Gruchott, Lukas Klein, Robert Fendrich, Thomas Zimmermann"

__license__ = """MIT License

                     Copyright (c) 2021 MUDCake Project

                     Permission is hereby granted, free of charge, to any person obtaining a copy
                     of this software and associated documentation files (the "Software"), to deal
                     in the Software without restriction, including without limitation the rights
                     to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
                     copies of the Software, and to permit persons to whom the Software is
                     furnished to do so, subject to the following conditions:

                     The above copyright notice and this permission notice shall be included in all
                     copies or substantial portions of the Software.

                     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
                     IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
                     FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
                     AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
                     LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
                     OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
                     SOFTWARE."""

__version__ = "1.0.0"
__maintainer__ = "Jan Gruchott"
__email__ = "mudcake@gmail.com"
__status__ = "Development"

import mysql
from mysql.connector import MySQLConnection
from termcolor import colored


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
        self.dictionary_cursor = self.database_path.cursor(dictionary=True)

    # print(colored('DB:', 'yellow'), 'xxx')

    def register_user(self, user):
        """
        insert user to database after user registration
        :param user: a user object
        :return: nothing
        """
        self.database_path.commit()
        self.cursor.execute("""
                                INSERT INTO mudcake.User
                                (UserID ,FirstName, LastName, UserName, Password, Email, isConfirmed)
                                VALUES 
                                (%s, %s, %s, %s, %s, %s, %s) 
                            """, (user.user_id, user.first_name, user.last_name, user.user_name, user.password,
                                  user.e_mail, user.confirmation))
        try:
            print(colored('DB:', 'yellow'), f"registered User '{user.user_id}'")
            self.database_path.commit()
        except IOError:
            print(colored('DB: register User failed', 'red'))
            pass

    def login_user(self, user):
        """
        checks if user is already in database, when client tries to login
        :param user: user object
        :return: returns the user from database if the user is exists in database
        """
        self.database_path.commit()
        self.cursor.execute("""
                                SELECT UserName, UserID, isConfirmed
                                From mudcake.User
                                WHERE (UserName = %s AND Password = %s)
                            """, (user.user_name, user.password))
        try:
            print(colored('DB:', 'yellow'), f"login User '{user.user_name}'")
            return self.cursor.fetchone()
        except IOError:
            print(colored('DB: login User failed', 'red'))
            return None

    def save_or_update_dungeon(self, dungeon):
        self.database_path.commit()
        self.cursor.execute(f"""
                                INSERT INTO mudcake.Dungeon
                                    (DungeonID, DungeonName, DungeonDescription, MaxPlayers, DungeonMasterID, Private)
                                VALUES 
                                    ("{dungeon.dungeon_data.dungeon_id}", "{dungeon.dungeon_data.name}", "{dungeon.dungeon_data.description}", 
                                    "{dungeon.dungeon_data.max_players}", "{dungeon.dungeon_data.dungeon_master_id}",
                                    "{int(dungeon.dungeon_data.private)}") 
                                ON DUPLICATE KEY UPDATE 
                                    DungeonID  = VALUES(DungeonID),
                                    DungeonName  = VALUES(DungeonName),
                                    MaxPlayers = VALUES(MaxPlayers),
                                    DungeonDescription = VALUES(DungeonDescription),
                                    DungeonMasterID  = VALUES(DungeonMasterID),
                                    Private  = VALUES(Private)
                            """)
        try:
            self.database_path.commit()
            print(colored('DB:', 'yellow'), f"save or update dungeon '{dungeon.dungeon_data.dungeon_id}'")
            return dungeon.dungeon_data.dungeon_id
        except IOError:
            print(colored('DB: save or update dungeon failed', 'red'))
            pass

    def get_user_id_by_email(self, email: str):
        '''
        reads the userid from the database belonging to the corresponding email
        :param email: email
        :return: returns the userid of the query 
        '''
        self.database_path.commit()
        self.cursor.execute(f"""
                                SELECT UserID
                                From mudcake.User
                                WHERE (Email = '{email}' )
                             """)
        try:
            print(colored('DB:', 'yellow'), f"get user id by email '{email}'")
            return (self.cursor.fetchone())[0]
        except IOError:
            print(colored('DB: get user id by email failed', 'red'))
            pass

    def get_dungeon_by_id(self, user_id: str):
        '''
        reads the dungeoninformation from the database belonging to the corresponding dungeonID
        :param dungeonID: id of the dungeon
        :return: value of query -> dungeonID, dungeonName, dungeonDescription 
        '''
        self.database_path.commit()
        self.cursor.execute(f"""
                    SELECT DungeonID, DungeonName, DungeonDescription
                    From mudcake.Dungeon
                    WHERE (DungeonMasterID = '{user_id}' )
                    """)
        try:
            print(colored('DB:', 'yellow'), f"get dungeon by user id '{user_id}'")
            return self.cursor.fetchall()
        except IOError:
            print(colored('DB: get dungeon by user id failed', 'red'))
            pass

    def update_password_by_user_id(self, user_id: str, password: str):
        """
        Updates UserPassword in Database
        :param user_id: UserID
        :param password: UserPassword
        :return: true if transaction is successful
        """
        self.database_path.commit()
        self.cursor.execute(f"""
                        UPDATE mudcake.User
                        SET Password = '{password}'
                        WHERE UserID = '{user_id}'
                        """)
        try:
            self.database_path.commit()
            print(colored('DB:', 'yellow'), f"update password by user id '{user_id}'")
            return True
        except IOError:
            print(colored('DB: update password by user id failed', 'red'))
            return False

    def delete_dungeon_by_id(self, dungeon_id: str):
        '''
        deletes the dungeon that belongs to the given dungeonid
        :param dungeonID: id of the dungeon
        '''
        self.database_path.commit()
        self.cursor.execute(f"""
                            DELETE
                            From mudcake.Dungeon
                            WHERE (DungeonID = '{dungeon_id}' )
                            """)
        try:
            self.database_path.commit()
            print(colored('DB:', 'yellow'), f"delete dungeon by id '{dungeon_id}'")
        except IOError:
            print(colored('DB: delete dungeon by id failed', 'red'))
            pass

    def delete_user_by_id(self, user_id):
        """
        deletes a user in database
        :param user_id: id of the user
        :return: true if transaction is successful
        """
        self.database_path.commit()
        self.cursor.execute(f"""
                            DELETE
                            From mudcake.User
                            WHERE (UserID = '{user_id}' )
                            """)
        try:
            self.database_path.commit()
            print(colored('DB:', 'yellow'), f"delete user by id '{user_id}'")
            return True
        except IOError:
            print(colored('DB: delete user by id failed', 'red'))
            return False

    def write_race_to_database(self, race, dungeon_id):
        '''
        insert a race object to database
        :param race: race object
        :param dungeon_id: id of dungeon 
        '''
        self.database_path.commit()
        self.cursor.execute(f"""
                                INSERT INTO mudcake.Race
                                    (DungeonID, RaceID, RaceName, RaceDescription)
                                VALUES 
                                    ("{dungeon_id}", "{race.race_id}", "{race.name}", "{race.description}")
                                ON DUPLICATE KEY UPDATE
                                    DungeonID=VALUES(DungeonID), RaceID=VALUES(RaceID), RaceName=VALUES(RaceName), RaceDescription=VALUES(RaceDescription)
                            """)

        try:
            self.database_path.commit()
            print(colored('DB:', 'yellow'), f"added race to db '{dungeon_id}'")
        except IOError:
            print(colored('DB: write race to database failed', 'red'))
            pass

    def write_class_to_database(self, class_object, dungeon_id):
        '''
        insert a class object to database
        :param class_object: class object
        :param dungeon_id: id of dungeon 
        '''
        self.database_path.commit()
        self.cursor.execute(f"""
                        INSERT INTO mudcake.Class
                          (DungeonID, ClassID, ClassName, ClassDescription, ItemID)
                        VALUES 
                          (%s, %s, %s, %s, %s)
                        ON DUPLICATE KEY UPDATE
                        DungeonID = VALUES(DungeonID), ClassID=VALUES(ClassID), ClassName=VALUES(ClassName), 
                            ClassDescription=VALUES(ClassDescription), ItemID = VALUES(ItemID)
                      """, (
        dungeon_id, class_object.class_id, class_object.name, class_object.description, class_object.item_id))
        try:
            self.database_path.commit()
            print(colored('DB:', 'yellow'), f"added class to db '{dungeon_id}'")
        except IOError:
            print(colored('DB: write class to database failed', 'red'))
            pass

    def write_room_to_database(self, room, dungeon_id):
        '''
        insert a room object to database
        :param room: room object
        :param dungeon_id: id of dungeon 
        '''
        self.database_path.commit()
        self.cursor.execute(f"""
                             INSERT INTO mudcake.Room
                                 (DungeonID, RoomID, RoomName, RoomDescription, CoordinateX, CoordinateY, 
                                    North, East, South, West, isStartingRoom, NpcID, ItemID)
                             VALUES 
                                 (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                            ON DUPLICATE KEY UPDATE
                            DungeonID = VALUES(DungeonID), RoomID = VALUES(RoomID), RoomName = VALUES(RoomName), RoomDescription = VALUES(RoomDescription), CoordinateX = VALUES(CoordinateX), CoordinateY=VALUES(CoordinateY),
                            North=VALUES(North),East=VALUES(East),South=VALUES(South),West=VALUES(West),isStartingRoom=VALUES(isStartingRoom),NpcID=VALUES(NpcID),ItemID=VALUES(ItemID)
                             """, (
            dungeon_id, room.room_id, room.room_name, room.room_description, room.coordinate_x, room.coordinate_y,
            int(room.north), int(room.east), int(room.south), int(room.west), int(room.is_start_room), room.npc_id,
            room.item_id))
        try:
            self.database_path.commit()
            print(colored('DB:', 'yellow'), f"added room to db '{dungeon_id}'")
        except IOError:
            print(colored('DB: write room to database failed', 'red'))
            pass

    def change_registration_status(self, user_id: str):
        '''
        updates the isConfirmed field from False(0) to True(1)
        :param user_id: id of user
        :return: true if transaction was successful, false if not 
        '''
        self.database_path.commit()
        self.cursor.execute(f"""
                    UPDATE mudcake.User
                    SET isConfirmed = 1
                    WHERE (UserID = '{user_id}')
                    """)
        try:
            self.database_path.commit()
            print(colored('DB:', 'yellow'), f"changes registrations status from user: '{user_id}'")
            return True
        except IOError:
            print(colored(f"DB: changing registration status from user: '{user_id}' failed", 'red'))
            return False

    def write_character_to_database(self, character, dungeon_id):
        self.database_path.commit()
        self.cursor.execute(f"""
                            INSERT INTO mudcake.Character 
                            (DungeonID, UserID, Lifepoints, CharacterName, CharacterDescription, 
                            RaceID, ClassID, RoomID, CharacterID) 
                            VALUES
                                (%s,%s,%s,%s,%s,%s,%s,%s, %s)
                            ON DUPLICATE KEY UPDATE
                            DungeonID = VALUES(DungeonID), UserID=VALUES(UserID),
                            Lifepoints = VALUES(Lifepoints), CharacterName=VALUES(CharacterName), 
                            CharacterDescription=VALUES(CharacterDescription),
                            RaceID=VALUES(RaceID), ClassID=VALUES(ClassID), RoomID=VALUES(RoomID), 
                            CharacterID=VALUES(CharacterID)""",
                            (dungeon_id, character.user_id, character.life_points, character.name,
                             character.description, character.race.race_id, character.class_obj.class_id,
                             character.room_id,
                             character.character_id))
        try:
            self.database_path.commit()
            print(colored('DB:', 'yellow'), f"write character to database '{character}'")
        except IOError:
            pass

    def write_npc_to_database(self, npc, dungeon_id):
        '''
        insert a npc object to database
        :param npc: npc object
        :param dungeon_id: id of dungeon 
        '''
        self.database_path.commit()
        self.cursor.execute(f"""
                                INSERT INTO mudcake.Npc
                                  (DungeonID, NpcID, NpcName, NpcDescription, ItemID)
                                VALUES 
                                    (%s,%s,%s,%s,%s)
                                ON DUPLICATE KEY UPDATE
                                DungeonID = VALUES(DungeonID), NpcID = VALUES(NpcID), NpcName = VALUES(NpcName), NpcDescription = VALUES(NpcDescription), ItemID = VALUES(ItemID)
                              """, (dungeon_id, npc.npc_id, npc.name, npc.description, npc.item))
        try:
            self.database_path.commit()
            print(colored('DB:', 'yellow'), f"write npc to database '{npc}'")
        except IOError:
            print(colored(f"DB: write item to database failed, npc: '{npc}'", 'red'))
            pass

    def write_item_to_database(self, item, dungeon_id):
        '''
        insert a item object to database
        :param item: item object
        :param dungeon_id: id of dungeon 
        '''
        self.database_path.commit()
        self.cursor.execute(f"""
                                      INSERT INTO mudcake.Item
                                          (DungeonID, ItemID, ItemName, ItemDescription)
                                      VALUES 
                                          (%s,%s,%s,%s)
                                    ON DUPLICATE KEY UPDATE 
                                    DungeonID = VALUES(DungeonID), ItemID = VALUES(ItemID), ItemName = VALUES(ItemName), ItemDescription =VALUES(ItemDescription)
                                      """, (dungeon_id, item.item_id, item.name, item.description))
        try:
            self.database_path.commit()
            print(colored('DB:', 'yellow'), f"write item to database '{item}'")
        except IOError:
            pass

    def get_character_by_dungeon_ID(self, dungeon_id: str):
        self.database_path.commit()
        self.cursor.execute(f"""
                    SELECT Lifepoints, CharacterName, CharacterDescription, ClassID, RaceID, UserID, RoomID
                    From mudcake.Character
                    WHERE (DungeonID = '{dungeon_id}')
                    """)
        try:
            print(colored('DB:', 'yellow'), f"get characters by dungeon id: '{dungeon_id}'")
            return self.cursor.fetchall()
        except IOError:
            pass

    def get_character_by_user_id(self, user_id: str, dungeon_id: str):
        self.database_path.commit()
        self.dictionary_cursor.execute(f"""
                                    SELECT 
                                    Character.CharacterID characterID,
                                    Character.CharacterName name,
                                    Character.CharacterDescription description,
                                    Character.Lifepoints health,
                                    Character.RoomID roomID,
                                    CharClass.ClassID classID,
                                    CharClass.ClassName className,
                                    CharClass.ClassDescription classDescription,
                                    CharRace.RaceID raceID,
                                    CharRace.RaceName raceName,
                                    CharRace.RaceDescription raceDescription
                                    FROM mudcake.Character
                                    LEFT JOIN
                                    mudcake.Class AS CharClass ON Character.ClassID = CharClass.ClassID
                                    LEFT JOIN
                                    mudcake.Race AS CharRace ON Character.RaceID = CharRace.RaceID
                                    WHERE (Character.DungeonID = '{dungeon_id}' AND Character.UserID = '{user_id}')    
                                    """)
        try:
            print(colored('DB:', 'yellow'), f"get character by user id: '{user_id}'")
            return self.dictionary_cursor.fetchone()
        except IOError:
            pass

    def get_class_by_dungeon_id(self, dungeon_id: str):
        self.database_path.commit()
        self.cursor.execute(f"""
                    SELECT ClassID, ClassName, ClassDescription
                    From mudcake.Class
                    WHERE (DungeonID = '{dungeon_id}')
                    """)
        try:
            print(colored('DB: ', 'yellow'), f'get class by dungeon id "{dungeon_id}"')
            return self.cursor.fetchall()
        except IOError:
            print(colored(f'DB: getting class by dungeonID. dungeonID: "{dungeon_id}"', 'red'))
            pass

    def get_race_by_dungeon_id(self, dungeon_id: str):
        self.database_path.commit()
        self.cursor.execute(f"""
                    SELECT RaceID, RaceName, RaceDescription
                    From mudcake.Race
                    WHERE (DungeonID = '{dungeon_id}')
                    """)
        try:
            print(colored('DB: ', 'yellow'), f'get race by dungeon id "{dungeon_id}"')
            return self.cursor.fetchall()
        except IOError:
            print(colored(f'DB: getting race by dungeonID. dungeonID: "{dungeon_id}"', 'red'))
            pass

    def get_npc_by_dungeon_id(self, dungeon_id: str):
        self.database_path.commit()
        self.cursor.execute(f"""
                    SELECT NpcID, NpcName, NpcDescription, ItemID
                    From mudcake.Npc
                    WHERE (DungeonID = '{dungeon_id}')
                    """)
        try:
            print(colored('DB: ', 'yellow'), f'get npc by dungeon id "{dungeon_id}"')
            return self.cursor.fetchall()
        except IOError:
            print(colored(f'DB: getting npc by dungeonID. dungeonID: "{dungeon_id}"', 'red'))
            pass

    def get_room_by_dungeon_id(self, dungeon_id: str):
        self.database_path.commit()
        self.cursor.execute(f"""
                    SELECT RoomID, RoomName, RoomDescription, CoordinateX, CoordinateY, North, East, South, West, 
                    isStartingRoom, NpcID, ItemID
                    From mudcake.Room
                    WHERE (DungeonID = '{dungeon_id}')
                    """)
        try:
            print(colored('DB: ', 'yellow'), f'get room by dungeon id "{dungeon_id}"')
            return self.cursor.fetchall()
        except IOError:
            print(colored(f'DB: getting room by dungeonID. dungeonID: "{dungeon_id}"', 'red'))
            pass

    def get_item_by_dungeon_id(self, dungeon_id: str):
        self.database_path.commit()
        self.cursor.execute(f"""
                    SELECT ItemID, ItemName, ItemDescription
                    From mudcake.Item
                    WHERE (DungeonID = '{dungeon_id}')
                    """)
        try:
            print(colored('DB: ', 'yellow'), f'get item by dungeon id "{dungeon_id}"')
            return self.cursor.fetchall()
        except IOError:
            print(colored(f'DB: getting item by dungeonID. dungeonID: "{dungeon_id}"', 'red'))
            pass

    def get_access_list_by_dungeon_id(self, dungeon_id: str):
        self.database_path.commit()
        self.dictionary_cursor.execute(f"""
                    SELECT  UserName userName, 
                            isAllowed
                    From mudcake.AccessList
                    WHERE (DungeonID = '{dungeon_id}')
                    """)
        try:
            print(colored('DB: ', 'yellow'), f'get AccessList by dungeon id "{dungeon_id}"')
            return self.dictionary_cursor.fetchall()
        except IOError:
            print(colored(f"DB: write AccessList to database failed, dungeon id: '{dungeon_id}'", 'red'))
            pass

    def get_dungeon_data_by_dungeon_id(self, dungeon_id: str):
        self.database_path.commit()
        self.cursor.execute(f"""
                    SELECT DungeonID, DungeonMasterID, DungeonName, DungeonDescription, Private, MaxPlayers
                    From mudcake.Dungeon
                    WHERE (DungeonID = '{dungeon_id}')
                    """)
        try:
            print(colored('DB: ', 'yellow'), f'get dungeon data by dungeon id "{dungeon_id}"')
            queryData = self.cursor.fetchall()
            print("QueryData: ", queryData)
            return queryData
        except IOError:
            print(colored(f"DB: get character by dungeon id failed, dungeon id: '{dungeon_id}'", 'red'))
            pass

    def get_discovered_rooms_by_user_dungeon_id(self, dungeon_id: str, user_id: str):
        self.database_path.commit()
        self.dictionary_cursor.execute(f"""
                        SELECT  UserID userID,
                                DungeonID dungeonID,
                                RoomID roomID
                        FROM mudcake.DiscoveredRoom
                        WHERE (DungeonID = '{dungeon_id}' AND UserID = '{user_id}')
                        """)
        try:
            print(colored('DB: ', 'yellow'), f'getting discovered rooms by dungeon and user. dungeonID: "{dungeon_id}"')
            return self.dictionary_cursor.fetchall()
        except IOError:
            pass

    def write_discovered_room_to_database(self, dungeon_id: str, user_id: str, room_id: str):
        self.cursor.execute(f"""
                        INSERT INTO mudcake.DiscoveredRoom
                            (RoomID, UserID, DungeonID)
                        VALUES
                            ('{room_id}', '{user_id}', '{dungeon_id}')
                        ON DUPLICATE KEY UPDATE
                            RoomID=VALUES(RoomID),
                            UserID=VALUES(UserID),
                            DungeonID=VALUES(DungeonID)
                        """)
        try:
            self.database_path.commit()
        except IOError:
            pass

    def get_inventory_by_dungeon_user_id(self, dungeon_id: str, user_id: str):
        self.database_path.commit()
        self.dictionary_cursor.execute(f"""
                    SELECT
                    InventoryItem.ItemID itemID, 
                    InventoryItem.ItemName itemName,
                    InventoryItem.ItemDescription itemDescription
                    From mudcake.Inventory
                    LEFT JOIN 
                    mudcake.Item as InventoryItem ON Inventory.ItemID = InventoryItem.ItemID
                    WHERE (Inventory.DungeonID = '{dungeon_id}' AND Inventory.UserID = '{user_id}')
                    """)
        try:
            print(colored('DB: ', 'yellow'), f'getting inventory by dungeon and user. dungeonID: "{dungeon_id}"')
            return self.dictionary_cursor.fetchall()
        except IOError:
            pass

    def check_user(self, user):
        """
        checks if user is already in database, when client is already logged in
        :param user: user object
        :return: returns true if credentials are still correct
        """
        self.database_path.commit()
        self.cursor.execute(f"""
            SELECT * 
            From mudcake.User
            WHERE (UserName = '{user.user_name}' AND UserID = '{user.user_id}' )
            """)
        try:
            query_data = self.cursor.fetchone()
            if query_data:
                return True
            else:
                return False
        except IOError:
            return False

    def user_status_on_access_list(self, user_name: str, dungeon_id: str):
        self.database_path.commit()
        self.cursor.execute(f"""
                                    SELECT IsAllowed
                                    FROM mudcake.AccessList
                                    WHERE (DungeonID = %s AND UserName = %s )
                                    """, (dungeon_id, user_name))
        try:
            variable = self.cursor.fetchone()
            print("Oh boy: ", variable)
            return variable
        except IOError:
            print("Error occurred by accessing AccessList")
            raise IOError

    #################### NEW #######################

    def get_all_rooms_by_dungeon_id_as_dict(self, dungeon_id: str):
        self.database_path.commit()
        self.dictionary_cursor.execute(
            f"""
                                    Select
                                        RoomID roomID,
                                        RoomName roomName,
                                        RoomDescription roomDescription,
                                        isStartingRoom isStartRoom,
                                        CoordinateX x,
                                        CoordinateY y,
                                        North north,
                                        East east,
                                        South south,
                                        West west,
                                        NpcID npcID,
                                        NpcName npcName,
                                        NpcDescription npcDescription,
                                        RoomItem.ItemID roomItemID,
                                        RoomItem.ItemName roomItemName,
                                        RoomItem.ItemDescription roomItemDescription,
                                        Item.ItemID npcItemID,
                                        Item.ItemDescription npcItemDesc,
                                        Item.ItemName npcItemName
                                    From
                                        mudcake.Room
                                    LEFT JOIN
                                        mudcake.Npc USING (NpcID)
                                    LEFT JOIN
                                        mudcake.Item ON Npc.ItemID = Item.ItemID
                                    LEFT JOIN
                                        mudcake.Item as RoomItem ON Room.ItemID = RoomItem.ItemID
                                    WHERE (Room.DungeonID = '{dungeon_id}')
                                    """)
        try:
            print(colored('DB:', 'yellow'), f'get rooms as dict. dungeonID: "{dungeon_id}"')
            datta = self.dictionary_cursor.fetchall()
            return datta
        except IOError:
            print(colored(f'DB: get rooms as dict failed. dungeonID "{dungeon_id}"', 'red'))

    def get_room_by_room_id_as_dict(self, dungeon_id: str, room_id: str):
        self.database_path.commit()
        self.dictionary_cursor.execute(
            f"""
                                    Select
                                        RoomID roomID,
                                        RoomName roomName,
                                        RoomDescription roomDescription,
                                        isStartingRoom isStartRoom,
                                        CoordinateX x,
                                        CoordinateY y,
                                        North north,
                                        East east,
                                        South south,
                                        West west,
                                        NpcID npcID,
                                        NpcName npcName,
                                        NpcDescription npcDescription,
                                        RoomItem.ItemID roomItemID,
                                        RoomItem.ItemName roomItemName,
                                        RoomItem.ItemDescription roomItemDescription,
                                        Item.ItemID npcItemID,
                                        Item.ItemDescription npcItemDesc,
                                        Item.ItemName npcItemName
                                    From
                                        mudcake.Room
                                    LEFT JOIN
                                        mudcake.Npc USING (NpcID)
                                    LEFT JOIN
                                        mudcake.Item ON Npc.ItemID = Item.ItemID
                                    LEFT JOIN
                                        mudcake.Item as RoomItem ON Room.ItemID = RoomItem.ItemID
                                    WHERE (Room.DungeonID = '{dungeon_id}' AND Room.RoomID = '{room_id}')
                                    """)
        try:
            print(colored('DB:', 'yellow'), f'get rooms as dict. dungeonID: "{dungeon_id}"')
            datta = self.dictionary_cursor.fetchone()
            return datta
        except IOError:
            print(colored(f'DB: get rooms as dict failed. dungeonID "{dungeon_id}"', 'red'))

    def get_all_classes_by_dungeon_id_as_dict(self, dungeon_id: str):
        self.database_path.commit()
        self.dictionary_cursor.execute(f"""
                                    SELECT ClassID classID,
                                           ClassName name,
                                           ClassDescription description,
                                           Item.ItemID itemID,
                                            Item.ItemName itemName,
                                            Item.ItemDescription itemDescription
                                    FROM mudcake.Class
                                    LEFT JOIN mudcake.Item ON Class.ItemID = Item.ItemID
                                    WHERE (Class.DungeonID ='{dungeon_id}')
                                    """)
        try:
            print(colored('DB: ', 'yellow'), f'get classes as dict. dungeonID "{dungeon_id}"')
            return self.dictionary_cursor.fetchall()
        except IOError:
            print(colored(f'DB: get classes as dict failed. dungeonID "{dungeon_id}"', 'red'))

    def get_all_races_by_dungeon_id_as_dict(self, dungeon_id: str):
        self.database_path.commit()
        self.dictionary_cursor.execute(f"""
                                    SELECT RaceID raceID,
                                           RaceName name,
                                           RaceDescription description,
                                           DungeonID dungeonID 
                                    FROM mudcake.Race
                                    WHERE (DungeonID = '{dungeon_id}' )
                                    """)
        try:
            print(colored('DB: ', 'yellow'), f'get races as dict. dungeonID: "{dungeon_id}"')
            return self.dictionary_cursor.fetchall()
        except IOError:
            print(colored(f'DB: get races as dict failed. dungeonID: "{dungeon_id}"', 'red'))

    def get_all_item_by_dungeon_id_as_dict(self, dungeon_id: str):
        self.database_path.commit()
        self.dictionary_cursor.execute(f"""
                                    SELECT ItemID itemID,
                                           ItemDescription description,
                                           ItemName name
                                    FROM mudcake.Item
                                    WHERE (DungeonID = '{dungeon_id}')
                                    """)
        try:
            print(colored('DB: ', 'yellow'), f'get items as dict. dungeonID: "{dungeon_id}"')
            return self.dictionary_cursor.fetchall()
        except IOError:
            print(colored(f'DB: get items as dict failed. dungeonID: "{dungeon_id}"', 'red'))

    def get_all_npc_by_dungeon_id_as_dict(self, dungeon_id: str):
        self.database_path.commit()
        self.dictionary_cursor.execute(f"""
                                    SELECT NpcID npcID,
                                           NpcName name,
                                           NpcDescription description,
                                           Item.ItemID itemID,
                                           Item.ItemName itemName,
                                            Item.ItemDescription itemDescription
                                    FROM mudcake.Npc
                                    LEFT JOIN mudcake.Item ON mudcake.Npc.ItemID=mudcake.Item.ItemID
                                    WHERE (Npc.DungeonID = '{dungeon_id}')
                                    """)
        try:
            print(colored('DB: ', 'yellow'), f'get npc as dict. dungeonID: "{dungeon_id}"')
            return self.dictionary_cursor.fetchall()
        except IOError:
            print(colored(f'DB: get npcs as dict failed. dungeonID: "{dungeon_id}"', 'red'))

    def get_access_list_by_dungeon_id_as_dict(self, dungeon_id: str):
        self.database_path.commit()
        self.dictionary_cursor.execute(f"""
                                    SELECT IsAllowed isAllowed,
                                           UserName name
                                    FROM mudcake.AccessList
                                    WHERE (DungeonID = '{dungeon_id}' )
                                    """, )
        try:
            print(colored('DB: ', 'yellow'), f'get accesslist as dict. dungeonID: "{dungeon_id}"')
            return self.dictionary_cursor.fetchall()
        except IOError:
            print(colored(f'DB: get accesslist as dict failed. dungeonID: "{dungeon_id}"', 'red'))

    def write_user_to_acceslist(self, access_list_user, dungeon_id):
        self.database_path.commit()
        self.cursor.execute(f"""
                                        INSERT INTO mudcake.AccessList
                                        (DungeonID, UserName, IsAllowed)
                                        VALUES
                                        (%s,%s,%s)
                                        ON DUPLICATE KEY UPDATE
                                        DungeonID = VALUES(DungeonID),
                                        UserName = VALUES(UserName),
                                        IsAllowed = VALUES(IsAllowed)
                            """, (dungeon_id, access_list_user['user_name'], access_list_user['is_allowed']))
        try:
            print(colored('DB: ', 'yellow'), f'write accesslist to database. dungeonID: "{dungeon_id}"')
            self.database_path.commit()
        except IOError:
            print(colored(f'DB: write accesslist to database failed. dungeonID: "{dungeon_id}"', 'red'))

    def get_item_by_class_id(self, class_id: str):
        self.database_path.commit()
        self.dictionary_cursor.execute(f"""
                                    SELECT Item.ItemID itemID, 
                                    Item.ItemName itemName, 
                                    Item.ItemDescription itemDescription
                                    
                                    FROM mudcake.Class
                                    LEFT JOIN
                                        mudcake.Item 
                                            ON Class.ItemID = Item.ItemID 
                                
                                    WHERE Class.ClassID = '{class_id}'
                                    """)
        try:
            return self.dictionary_cursor.fetchone()
        except IOError:
            print("Fetching Item from Class failed")
            pass

    def add_item_to_inventory(self, item_id: str, user_id: str, dungeon_id: str):
        self.database_path.commit()
        self.cursor.execute(f"""
                         INSERT INTO mudcake.Inventory
                         (ItemID, UserID, DungeonID)
                         VALUES
                         ('{item_id}', '{user_id}', '{dungeon_id}')
                         ON DUPLICATE KEY UPDATE
                         ItemID = VALUES(ItemID),
                         UserID = VALUES(UserID),
                         DungeonID = VALUES(DungeonID)
                        """)
        try:
            self.database_path.commit()
        except IOError:
            print("Error occurred during add_item_to_inventory")
            pass

    def delete_user_from_accesslist(self, username, dungeon_id):
        self.database_path.commit()
        self.cursor.execute(f"""
                                DELETE 
                                FROM mudcake.AccessList
                                WHERE UserName = '{username}' AND DungeonID = '{dungeon_id}'
                               """)
        try:
            self.database_path.commit()
        except IOError:
            print("Error occurred during add_item_to_inventory")
            pass

    def remove_item_from_inventory(self, item_id: str, user_id: str, dungeon_id: str):
        self.database_path.commit()
        self.cursor.execute(f"""
                                DELETE
                                FROM mudcake.Inventory
                                WHERE ItemID = '{item_id}' AND UserID = '{user_id}' AND DungeonID = '{dungeon_id}'
                            """)
        try:
            self.database_path.commit()
        except IOError:
            pass

    def set_character_health(self, lifepoints: int, user_id: str, dungeon_id: str):
        self.database_path.commit()
        self.cursor.execute(f"""
                                UPDATE mudcake.Character
                                SET Lifepoints = '{lifepoints}'
                                WHERE UserID = '{user_id}' AND DungeonID = '{dungeon_id}'
                            """)
        try:
            self.database_path.commit()
        except IOError:
            pass

    def remove_room_by_room_id(self, room_id: str):
        self.database_path.commit()
        self.cursor.execute(f"""
                                DELETE
                                FROM mudcake.Room
                                WHERE RoomID = '{room_id}'
                            """)
        try:
            self.database_path.commit()
        except IOError:
            pass
