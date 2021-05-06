import asyncio
import websockets
import json


class WebSocketHandler:
    def __init__(self):
        self.all_connections = set()


    async def handle(self,websocket, path):
        try:
            #jeder Socket/Spieler trägt sich in Set ein
            self.all_connections.add(websocket)

            #immer wenn die Instanz eine Nachricht sendet...
            async for msg in websocket:
                data = json.loads(msg)
                print(f"received: {data}")

                reply_message = {
                    'content': 'hallo wie gehts'
                }

                await websocket.send(json.dumps(reply_message))

        finally:
            #Beim Disconnecten trägt sich die Instanz aus dem Set aus
            self.all_connections.discard(websocket)
