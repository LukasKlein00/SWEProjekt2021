import asyncio
import websockets
import json

allConnections = set()


async def WebSocketHandler(websocket, path):
    try:
        #jeder Socket/Spieler trägt sich in Set ein
        allConnections.add(websocket)

        #immer wenn die Instanz eine Nachricht sendet...
        async for msg in websocket:
            data = json.loads(msg)
            print(f"received: {data}")

            replyMessage = {
                'content': 'hallo wie gehts'
            }

            await websocket.send(json.dumps(replyMessage))

    finally:
        #Beim Disconnecten trägt sich die Instanz aus dem Set aus
        allConnections.discard(websocket)
