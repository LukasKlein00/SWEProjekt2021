import json
from termcolor import colored
from DungeonPackage.DungeonData import DungeonData
from DungeonDirector.ActiveDungeonHandler import ActiveDungeonHandler
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
            self.sio.enter_room(sid, data)
            print(sid, data['message'])

        @self.sio.event
        def publish(sid, data):
            self.sio.enter_room(sid, data)
            self.activeDungeonHandler.dungeon_join(data)
            self.activeDungeonHandler.sid_of_dungeon_master[data] = sid

        @self.sio.event
        def disconnect(sid):
            print('disconnect: ', sid)