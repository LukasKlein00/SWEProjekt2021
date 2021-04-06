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

def saveOrUpdateMap(dungeonID, dungeonContent):
    conn = connect()
    c = conn.cursor()
    query = f"""INSERT INTO mudcake.dungeons (dungeonID, dungeonContent) VALUES
    (${dungeonID}, ${dungeonContent}) ON DUPLICATE KEY UPDATE dungeonID=f{dungeonID}, dungeonContent=${dungeonContent}"""
    try:
        c.execute(query)
        print("added")
    except:
        print("fail adding/updating Dungeon")
        conn.close()
        return 0
    return "successful"
    