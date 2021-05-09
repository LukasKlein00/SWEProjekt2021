import mysql
import mysql.connector
from mysql.connector import errorcode
import unittest
from mock import patch
from unittest import TestCase
import utils

MYSQL_USER = "jack"
MYSQL_PASSWORD = "123123"
MYSQL_DB = "mudcake_test"
MYSQL_HOST = "193.196.53.67"
MYSQL_PORT = "1189"


class MockDB(TestCase):

    @classmethod
    def setupClass(cls):
        ref = mysql.connector.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD
        )
        cursor = ref.cursor(dictionary=True)
        try:
            cursor.execute("DROP DATABASE {}".format(MYSQL_DB))
            cursor.close()
            print("DB dropped")
        except mysql.connector.Error as err:
            print("{}{}".format(mysql, err))

            # create database
        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(MYSQL_DB))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)
        ref.database = MYSQL_DB

        # create table

        query = """
        CREATE TABLE `AccessList` ( `DungeonID` varchar(450) NOT NULL, `IsAllowed` tinyint DEFAULT NULL, 
        `UserID` varchar(45) NOT NULL, PRIMARY KEY (`DungeonID`,`UserID`), KEY `UserIDAccessList_idx` (`UserID`), 
        CONSTRAINT `DungeonIDAccessList` FOREIGN KEY (`DungeonID`) REFERENCES `Dungeon` (`DungeonID`) ON DELETE 
        CASCADE ON UPDATE CASCADE, CONSTRAINT `UserIDAccessList` FOREIGN KEY (`UserID`) REFERENCES `User` (`UserID`) 
        ON DELETE CASCADE ON UPDATE CASCADE ) / CREATE TABLE `Character` ( `CharacterID` varchar(45) NOT NULL, 
        `Lifepoints` int DEFAULT NULL, `CharacterName` varchar(45) DEFAULT NULL, `CharacterDescription` varchar(450) 
        DEFAULT NULL, `ClassID` varchar(45) DEFAULT NULL, `RaceID` varchar(45) DEFAULT NULL, `UserID` varchar(45) NOT 
        NULL, `RoomID` varchar(45) DEFAULT NULL, `DungeonID` varchar(450) NOT NULL, PRIMARY KEY (`CharacterID`,
        `DungeonID`,`UserID`), KEY `UserIDCharacter_idx` (`UserID`), KEY `DungeonIDCharacter_idx` (`DungeonID`), 
        KEY `ClassIDCharacter_idx` (`ClassID`), KEY `RaceIDCharacter_idx` (`RaceID`), CONSTRAINT `ClassIDCharacter` 
        FOREIGN KEY (`ClassID`) REFERENCES `Class` (`ClassID`) ON DELETE SET NULL ON UPDATE CASCADE, CONSTRAINT 
        `DungeonIDCharacter` FOREIGN KEY (`DungeonID`) REFERENCES `Dungeon` (`DungeonID`) ON DELETE CASCADE ON UPDATE 
        CASCADE, CONSTRAINT `RaceIDCharacter` FOREIGN KEY (`RaceID`) REFERENCES `Race` (`RaceID`) ON DELETE SET NULL 
        ON UPDATE CASCADE, CONSTRAINT `UserIDCharacter` FOREIGN KEY (`UserID`) REFERENCES `User` (`UserID`) ON DELETE 
        CASCADE ON UPDATE CASCADE ) / CREATE TABLE `Class` ( `ClassID` varchar(45) NOT NULL, `ClassName` varchar(45) 
        DEFAULT NULL, `ClassDescription` varchar(450) DEFAULT NULL, `DungeonID` varchar(450) NOT NULL, 
        `ItemID` varchar(45) DEFAULT NULL, PRIMARY KEY (`ClassID`,`DungeonID`), KEY `DungeonIDClass_idx` (
        `DungeonID`), KEY `ItemIDClass_idx` (`ItemID`), CONSTRAINT `DungeonIDClass` FOREIGN KEY (`DungeonID`) 
        REFERENCES `Dungeon` (`DungeonID`) ON DELETE CASCADE ON UPDATE CASCADE, CONSTRAINT `ItemIDClass` FOREIGN KEY 
        (`ItemID`) REFERENCES `Item` (`ItemID`) ON DELETE SET NULL ON UPDATE CASCADE ) / CREATE TABLE 
        `DiscoveredRoom` ( `DiscoveredRoomID` varchar(45) NOT NULL, `RoomID` varchar(45) NOT NULL, PRIMARY KEY (
        `DiscoveredRoomID`,`RoomID`), KEY `RoomIDDiscoveredRoom_idx` (`RoomID`), CONSTRAINT `RoomIDDiscoveredRoom` 
        FOREIGN KEY (`RoomID`) REFERENCES `Room` (`RoomID`) ON DELETE CASCADE ON UPDATE CASCADE ) / CREATE TABLE 
        `Dungeon` ( `DungeonID` varchar(450) NOT NULL, `MaxPlayers` int DEFAULT NULL, `DungeonName` varchar(45) 
        DEFAULT NULL, `DungeonDescription` varchar(450) DEFAULT NULL, `Private` tinyint DEFAULT NULL, 
        `DungeonMasterID` varchar(45) NOT NULL, PRIMARY KEY (`DungeonID`,`DungeonMasterID`), KEY `UserIDDungeon_idx` 
        (`DungeonMasterID`), CONSTRAINT `UserIDDungeon` FOREIGN KEY (`DungeonMasterID`) REFERENCES `User` (`UserID`) 
        ON DELETE CASCADE ON UPDATE CASCADE ) / CREATE TABLE `Inventory` ( `InventoryID` varchar(45) NOT NULL, 
        `ItemID` varchar(45) NOT NULL, `CharacterID` varchar(45) NOT NULL, PRIMARY KEY (`InventoryID`,`ItemID`,
        `CharacterID`), KEY `CharacterIDInventory_idx` (`CharacterID`), KEY `ItemIDInventory_idx` (`ItemID`), 
        CONSTRAINT `CharacterIDInventory` FOREIGN KEY (`CharacterID`) REFERENCES `Character` (`CharacterID`) ON 
        DELETE CASCADE ON UPDATE CASCADE, CONSTRAINT `ItemIDInventory` FOREIGN KEY (`ItemID`) REFERENCES `Item` (
        `ItemID`) ON DELETE CASCADE ON UPDATE CASCADE ) / CREATE TABLE `Item` ( `ItemID` varchar(45) NOT NULL, 
        `ItemDescription` varchar(450) DEFAULT NULL, `ItemName` varchar(45) DEFAULT NULL, `DungeonID` varchar(450) 
        NOT NULL, PRIMARY KEY (`ItemID`,`DungeonID`), KEY `DungeonIDItem_idx` (`DungeonID`), CONSTRAINT 
        `DungeonIDItem` FOREIGN KEY (`DungeonID`) REFERENCES `Dungeon` (`DungeonID`) ON DELETE CASCADE ON UPDATE 
        CASCADE ) / CREATE TABLE `Npc` ( `NpcID` varchar(45) NOT NULL, `NpcName` varchar(45) DEFAULT NULL, 
        `NpcDescription` varchar(450) DEFAULT NULL, `DungeonID` varchar(450) NOT NULL, `ItemID` varchar(45) DEFAULT 
        NULL, PRIMARY KEY (`NpcID`,`DungeonID`), KEY `ItemIDNpc_idx` (`ItemID`), KEY `DungeonIDNpc_idx` (
        `DungeonID`), CONSTRAINT `DungeonIDNpc` FOREIGN KEY (`DungeonID`) REFERENCES `Dungeon` (`DungeonID`) ON 
        DELETE CASCADE ON UPDATE CASCADE, CONSTRAINT `ItemIDNpc` FOREIGN KEY (`ItemID`) REFERENCES `Item` (`ItemID`) 
        ON DELETE CASCADE ON UPDATE CASCADE ) / CREATE TABLE `Race` ( `RaceID` varchar(45) NOT NULL, `RaceName` 
        varchar(45) DEFAULT NULL, `RaceDescription` varchar(450) DEFAULT NULL, `DungeonID` varchar(450) NOT NULL, 
        PRIMARY KEY (`RaceID`,`DungeonID`), KEY `DungeonIDRoom_idx` (`DungeonID`), CONSTRAINT `DungeonIDRace` FOREIGN 
        KEY (`DungeonID`) REFERENCES `Dungeon` (`DungeonID`) ON DELETE CASCADE ON UPDATE CASCADE ) / CREATE TABLE 
        `Room` ( `RoomID` varchar(45) NOT NULL, `isStartingRoom` tinyint DEFAULT NULL, `RoomDescription` varchar(450) 
        DEFAULT NULL, `RoomName` varchar(45) DEFAULT NULL, `CoordinateX` int DEFAULT NULL, `CoordinateY` int DEFAULT 
        NULL, `North` tinyint DEFAULT NULL, `East` tinyint DEFAULT NULL, `South` tinyint DEFAULT NULL, `West` tinyint 
        DEFAULT NULL, `DungeonID` varchar(450) NOT NULL, `NpcID` varchar(45) DEFAULT NULL, `ItemID` varchar(45) 
        DEFAULT NULL, PRIMARY KEY (`RoomID`,`DungeonID`), KEY `NpcID_idx` (`NpcID`), KEY `ItemID_idx` (`ItemID`), 
        KEY `DungeonIDRoom_idx` (`DungeonID`), CONSTRAINT `DungeonIDRoom` FOREIGN KEY (`DungeonID`) REFERENCES 
        `Dungeon` (`DungeonID`) ON DELETE CASCADE ON UPDATE CASCADE, CONSTRAINT `ItemIDRoom` FOREIGN KEY (`ItemID`) 
        REFERENCES `Item` (`ItemID`) ON DELETE CASCADE ON UPDATE CASCADE, CONSTRAINT `NpcIDRoom` FOREIGN KEY (
        `NpcID`) REFERENCES `Npc` (`NpcID`) ON DELETE CASCADE ON UPDATE CASCADE ) / CREATE TABLE `User` ( `UserID` 
        varchar(45) NOT NULL, `FirstName` varchar(45) DEFAULT NULL, `LastName` varchar(45) DEFAULT NULL, `UserName` 
        varchar(45) DEFAULT NULL, `Password` varchar(45) DEFAULT NULL, `Email` varchar(45) DEFAULT NULL, 
        `isConfirmed` tinyint DEFAULT NULL, PRIMARY KEY (`UserID`) ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 
        COLLATE=utf8mb4_0900_ai_ci;
        """
        try:
            cursor.execute(query)
            ref.commit()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("test_table already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

        # insert data

        insert_data_query = """INSERT INTO `test_table` (`id`, `text`, `int`) VALUES
                              ('1', 'test_text', 1),
                              ('2', 'test_text_2',2)"""
        try:
            cursor.execute(insert_data_query)
            ref.commit()
        except mysql.connector.Error as err:
            print("Data insertion to test_table failed \n" + err)
        cursor.close()
        ref.close()

        test_config = {
            'host': MYSQL_HOST,
            'user': MYSQL_USER,
            'password': MYSQL_PASSWORD,
            'database': MYSQL_DB,
        }
        cls.mock_db_config = patch.dict(utils.config, test_config)

    @classmethod
    def tearDownClass(cls):
        ref = mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
        )
        cursor = ref.cursor(dictionary=True)

        # drop test database
        try:
            cursor.execute("DROP DATABASE {}".format(MYSQL_DB))
            ref.commit()
            cursor.close()
        except mysql.connector.Error as err:
            print("Database {} does not exists. Dropping db failed".format(MYSQL_DB))
        ref.close()
