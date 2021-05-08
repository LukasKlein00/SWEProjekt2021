import asyncio
import websockets
import json
import random

from termcolor import colored

from DungeonPackage.DungeonData import DungeonData
from DungeonDirector.ActiveDungeonHandler import ActiveDungeonHandler

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
            self.all_connections.discard(websocket)
            
                        jans_crack_hauscount = 0
            thommys_trap_hauscount = 0
            print('connect: ', sid)
            if random.random() > 0.5:
                self.sio.enter_room(sid, 'Jans Crackhaus')
                jans_crack_hauscount += 1
                self.sio.emit('room_count', jans_crack_hauscount, to='Jans Crackhaus')
            else:
                self.sio.enter_room(sid, 'Thommys Traphaus')
                thommys_trap_hauscount += 1
                self.sio.emit('room_count', thommys_trap_hauscount, to='Thommys Traphaus')"""


import eventlet
import socketio
class SocketIOHandler:
    def __init__(self):
        self.sio = socketio.Server(cors_allowed_origins='*')
        self.app = socketio.WSGIApp(self.sio)
        self.active_dungeons = []
        self.activeDungeonHandler = ActiveDungeonHandler()


        @self.sio.event
        def connect(sid, environ):
            dungeon_data_list = []
            print(colored(f"Dungeon Data List: {dungeon_data_list}", 'red'))
            print(colored(f"Dungeon Handler List: {self.activeDungeonHandler.active_dungeon_ids}", 'red'))
            for dungeon_ID  in self.activeDungeonHandler.active_dungeon_ids:
                dungeon_data = DungeonData(dungeon_id=dungeon_ID)
                dungeon_dict = {"dungeonID": dungeon_data.dungeon_id, "dungeonMasterID": dungeon_data.dungeon_master_id,
                                "dungeonName": dungeon_data.name, "dungeonDescription": dungeon_data.description,
                                "maxPlayers": dungeon_data.max_players, "accessList": dungeon_data.access_list,
                                "private": dungeon_data.private}
                dungeon_data_list.append(dungeon_dict)
                print(colored(dungeon_dict, 'green'))
            if len(dungeon_data_list) != 0:
                self.sio.emit('make_dungeon_available', json.dumps(dungeon_data_list), broadcast=True)
                print(colored("publish successful", 'green'))

        @self.sio.event
        def message(sid, data):
            print('message: ', data)
            self.sio.emit('message')

        @self.sio.event
        def joined(sid, data):
            print(sid, data['message'])

        @self.sio.event
        def publish(sid, data):
            self.sio.enter_room(sid, data)
            self.activeDungeonHandler.dungeon_join(data)

        @self.sio.event
        def disconnect(sid):
            print('disconnect: ', sid)