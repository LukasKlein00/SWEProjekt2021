import asyncio
import websockets
import json


class WebSocketHandler:
    def __init__(self):
        self.allConnections = set()


    async def handle(self,websocket, path):
        try:
            #jeder Socket/Spieler trägt sich in Set ein
            self.allConnections.add(websocket)

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
            self.allConnections.discard(websocket)
