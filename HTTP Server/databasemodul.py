import sqlite3
import uuid


def addUser(Username, Vorname, Nachname, Passwort):
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()
    Token = uuid.uuid4()
    query = f"INSERT INTO accounts VALUES ('{Username}','{Vorname}','{Nachname}','{Passwort}','{Token}')"
    try:
        c.execute(query)
        added = True
    except:
        added = False
    conn.commit()
    conn.close()
    return added

def checkLogin(Username,Passwort):
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()
    query = f"SELECT token FROM accounts WHERE (username ='{Username}' AND passwort = '{Passwort}')"
    c.execute(query)
    try:
        token = c.fetchone()[0]
    except:
        token = 0
    conn.close()
    return token

def checkToken(Token):
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()
    query = f"SELECT username FROM accounts WHERE (token ='{Token}')"
    c.execute(query)
    try:
        username = c.fetchone()[0]
    except:
        username = 0
    conn.close()
    return username