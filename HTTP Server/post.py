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
        print("fail adding/updating Dungeon")
        conn.close()
        return 0
    return "successful"
    