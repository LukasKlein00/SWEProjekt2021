import uuid
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

def saveOrUpdateDungeon(dungeon):
    conn = connect()
    c = conn.cursor()
    query = """
        INSERT INTO mudcake.dungeons 
            (dungeonID, dungeonName, dungeonDescription, maxPlayers, dungeonMasterID, rooms, races, classes, items, npcs, private, whiteList, blackList)
        VALUES 
            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
        ON DUPLICATE KEY UPDATE 
            dungeonName  = VALUES(dungeonName),
            dungeonDescription  = VALUES(dungeonDescription),
            maxPlayers = VALUES(maxPlayers),
            dungeonMasterID  = VALUES(dungeonMasterID),
            rooms  = VALUES(rooms),
            races  = VALUES(races),
            classes  = VALUES(classes),
            items  = VALUES(items),
            npcs  = VALUES(npcs),
            private = VALUES(private),
            whiteList = VALUES(whiteList),
            blackList = VALUES(blackList)
                   """ 
    variables = (dungeon['dungeonID'], dungeon['dungeonName'], dungeon['dungeonDescription'], dungeon['maxPlayers'], dungeon['dungeonMasterID'], json.dumps(dungeon['rooms']), json.dumps(dungeon['races']), json.dumps(dungeon['classes']), json.dumps(dungeon['items']), json.dumps(dungeon['npcs']), dungeon['private'], json.dumps(dungeon['whiteList']), json.dumps(dungeon['blackList']))
    try:
        c.execute(query, variables)
        conn.commit()
    except IOError:
        pass
    conn.close()
    return "successful"

def regiserUser(user):
    conn = connect()
    c = conn.cursor()
    query = """
    INSERT INTO mudcake.accounts 
            (username, vorname, nachname, passwort, userID, email)
        VALUES 
            (%s, %s, %s, %s, %s, %s) 
    """
    variables = (user['username'], user['firstName'],user['lastName'], user['password'], user['userID'], user['email'])
    try:
        c.execute(query, variables)
        conn.commit()
    except IOError:
        pass
    conn.close()
    return "successful"

def loginUser(user):
    conn = connect()
    c = conn.cursor() 
    query = """
    SELECT username, userID
    From mudcake.accounts 
    WHERE (username = %s AND passwort = %s)
    """
    variables = (user['username'], user['password'])
    c.execute(query, variables)
    try:
        username = c.fetchone()
    except:
        username = 0
    conn.close()
    return username  

def getMyDungeons(userID):
    conn = connect()
    c = conn.cursor()
    query = f"""
    SELECT dungeonID, dungeonName, dungeonDescription
    From mudcake.dungeons 
    WHERE (dungeonMasterID = '{userID}')
    """
    c.execute(query)
    try:
        dungeons = c.fetchall()
    except:
        dungeons = 0
    conn.close()
    return dungeons

def getDungeon(dungeonID):
    conn = connect()
    c = conn.cursor()
    query = f"""
    SELECT *
    From mudcake.dungeons 
    WHERE (dungeonID = '{dungeonID}')
    """
    c.execute(query)
    try:
        dungeons = c.fetchone()
    except:
        dungeons = 0
    conn.close()
    return dungeons     