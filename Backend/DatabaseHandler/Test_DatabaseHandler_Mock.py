import mysql
import mysql.connector
from mysql.connector import errorcode
import unittest
from mock import patch
from unittest import TestCase
import utils

MYSQL_USER = "jack"
MYSQL_PASSWORD = "123123"
MYSQL_DB = "mudcake"
MYSQL_HOST = "193.196.53.67"
MYSQL_PORT = "1189"

class MockDB(TestCase):

    def SetupClass(cls):
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

        query = """CREATE TABLE `test_table` (
                    `id` varchar(30) NOT NULL PRIMARY KEY ,
                    `text` text NOT NULL,
                    `int` int NOT NULL
                  )"""
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
                host="193.196.53.67",
                user="jack",
                password="123123"
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


