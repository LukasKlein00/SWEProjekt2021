import uuid
import mysql.connector


def connect():
    mydb = mysql.connector.connect(
        host="193.196.53.67",
        port="1189",
        user="jack",
        password="123123"
    )
    return mydb

def addUser(Username, Vorname, Nachname, Passwort):
    conn = connect()
    c = conn.cursor()
    Token = uuid.uuid4()
    query = f"INSERT INTO mudcake.accounts VALUES ('{Username}','{Vorname}','{Nachname}','{Passwort}','{Token}')"
    try:
        c.execute(query)
        added = True
    except:
        added = False
    conn.commit()
    conn.close()
    return added

def checkLogin(Username,Passwort):
    conn = connect()
    c = conn.cursor()
    query = f"SELECT token FROM mudcake.accounts WHERE (username ='{Username}' AND passwort = '{Passwort}')"
    c.execute(query)
    try:
        token = c.fetchone()[0]
    except:
        token = 0
    conn.close()
    return token

def checkToken(Token):
    conn = connect()
    c = conn.cursor()
    query = f"SELECT username FROM mudcake.accounts WHERE (token ='{Token}')"
    c.execute(query)
    try:
        username = c.fetchone()[0]
    except:
        username = 0
    conn.close()
    return username