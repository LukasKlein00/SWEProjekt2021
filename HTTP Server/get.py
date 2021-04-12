import mysql.connector
import json

def connect():
    mydb = mysql.connector.connect(
        host="193.196.53.67",
        port="1189",
        user="jack",
        password="123123"
    )
    return mydb