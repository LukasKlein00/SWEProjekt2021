import asyncio
import websockets
import json


"""class WebSocketHandler:
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
            self.all_connections.discard(websocket)"""


import eventlet
import socketio
class SocketIOHandler:
    def __init__(self):
        self.sio = socketio.Server()
        self.app = socketio.WSGIApp(self.sio, static_files={
            '/': './index.html'
        })


        @self.sio.event
        def connect(sid, environ):
            print('connect: ', sid)

        @self.sio.event
        def my_message(sid, data):
            print('message: ', data)
            self.sio.emit('onmessage')

        @self.sio.event
        def disconnect(sid):
            print('disconnect: ', sid)