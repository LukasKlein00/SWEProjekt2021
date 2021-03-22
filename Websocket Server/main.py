import asyncio
import websockets
import json

t = {
    'method': 'chat',
    'content': {
        'content': 'hallo wie gehts',
        'playerName': 'GüntherGrünschnabel',
        'mapID': 2,
        'receiver': 'dungeonchat',
    }
}
dummyData = json.dumps(t)




#Set, wo alle Verbunden Instanzen gespeichert werden
allConnections = set()


#Server
async def server(websocket, path):
    try:
        #immer wenn eine Instanz eine Nachricht sendet...
        async for msg in websocket:
            data = json.loads(msg)
            if data['methode'] == 'playerJoin':
                playerJoinInfos = data['content']
                allConnections.add({
                    'socket': websocket,
                    'mapID': playerJoinInfos['mapID'],
                    'playerName': playerJoinInfos['playerName']
                })

            if data['methode'] == 'chat':
                message = data['content']

                if message['receiver'] == 'dungeonchat':
                    replyMessage= {
                            'content': 'hallo wie gehts',
                            'playerName': 'GüntherGrünschnabel',
                            'mapID': 2,
                            'receiver': 'dungeonchat',
                        }
                    for player in allConnections:
                        if player['mapID'] == message['mapID']:
                            #sendet Antwort an alle Spieler des Dungeons
                            await player['socket'].send(json.dumps(replyMessage))
    finally:
        #Beim Disconnecten trägt sich die Instanz aus dem Set aus
        for player in allConnections:
            if player['socket'] == websocket:
                allConnections.discard(player)



#Main-Methode wird beim Starten der Datei ausgeführt
if __name__ == '__main__':
    print('Starting WebsocketServer... \n')
    start_server = websockets.serve(server, '', 1187)
    print('Server is running!')
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()