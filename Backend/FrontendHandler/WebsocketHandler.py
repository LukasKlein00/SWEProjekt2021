import json
import uuid

from termcolor import colored
from json import JSONEncoder
from BackendServices.AccessManager import AccessManager
from BackendServices.DungeonManager import DungeonManager
from DungeonPackage.DungeonData import DungeonData
from DungeonPackage.Character import Character
from DungeonDirector.ActiveDungeonHandler import ActiveDungeonHandler
import socketio


# TODO: user access management



class SocketIOHandler:
    def __init__(self):
        self.sio = socketio.Server(cors_allowed_origins='*', async_mode='eventlet')
        self.sio.logger.disabled = True
        self.app = socketio.WSGIApp(self.sio)
        self.active_dungeons = []
        self.activeDungeonHandler = ActiveDungeonHandler()
        self.dungeon_manager = DungeonManager()
        self.access_manager = AccessManager()

        @self.sio.event
        def send_join_request_answer(sid, data):
            answer = data["isAllowed"]
            for socket in self.activeDungeonHandler.user_sid[data['userID']]:
                self.sio.emit("on_join_request_answer", answer, to=socket)

        @self.sio.event
        def on_login(sid, data):
            self.sio.save_session(sid, {'userID': data['userID'], 'userName': data['username']})
            self.activeDungeonHandler.user_sid[data['userID']] = []
            array = self.activeDungeonHandler.user_sid[data['userID']]
            array.append(sid)
            self.activeDungeonHandler.user_sid[data['userID']] = array
            print("USERSIDS:", self.activeDungeonHandler.user_sid[data['userID']])

        @self.sio.event
        def on_home(sid):
            dungeon_data_list = []
            for dungeon_ID in self.activeDungeonHandler.active_dungeon_ids:
                if self.activeDungeonHandler.sid_of_dungeon_master[dungeon_ID] != sid:
                    dungeon_data = DungeonData(dungeon_id=dungeon_ID).load_data(dungeon_id=dungeon_ID)
                    dungeon_dict = {"dungeonID": dungeon_data.dungeon_id,
                                    "dungeonMasterID": dungeon_data.dungeon_master_id,
                                    "dungeonName": dungeon_data.name, "dungeonDescription": dungeon_data.description,
                                    "maxPlayers": dungeon_data.max_players, "accessList": dungeon_data.access_list,
                                    "private": dungeon_data.private}
                    dungeon_data_list.append(dungeon_dict)
                    print(colored(dungeon_dict, 'green'))
            self.sio.emit('make_dungeon_available', json.dumps(dungeon_data_list), to=sid)
            print(colored("publish successful", 'green'))

        @self.sio.event
        def connect(sid, environ, data):
            dungeon_data_list = []
            print(colored(f"Dungeon Data List: {dungeon_data_list}", 'red'))
            print(colored(f"Dungeon Handler List: {self.activeDungeonHandler.active_dungeon_ids}", 'red'))
            for dungeon_ID in self.activeDungeonHandler.active_dungeon_ids:
                if self.activeDungeonHandler.sid_of_dungeon_master[dungeon_ID] != sid:
                    dungeon_data = DungeonData(dungeon_id=dungeon_ID).load_data(dungeon_id=dungeon_ID)
                    dungeon_dict = {"dungeonID": dungeon_data.dungeon_id,
                                    "dungeonMasterID": dungeon_data.dungeon_master_id,
                                    "dungeonName": dungeon_data.name, "dungeonDescription": dungeon_data.description,
                                    "maxPlayers": dungeon_data.max_players, "accessList": dungeon_data.access_list,
                                    "private": dungeon_data.private}
                    dungeon_data_list.append(dungeon_dict)
                    print(colored(dungeon_dict, 'green'))
            if len(dungeon_data_list) != 0:
                self.sio.emit('make_dungeon_available', json.dumps(dungeon_data_list), broadcast=True)
                print(colored("publish successful", 'green'))


        #TODO: mit jack klären, dass aktive dungeons die vom dungeonmaster verlassen wurden beim dungeon master als
        # aktiv gekennzeicnet werden und dungeon ein beenden button bekommen
        @self.sio.event
        def disconnect(sid):
            if sid in self.activeDungeonHandler.sid_of_dungeon_master.values():
                dungeon_data_list = []
                self.activeDungeonHandler.dungeon_leave(self.sio.get_session(sid)['dungeonID'])
                if self.activeDungeonHandler.active_dungeon_ids.__len__() != 0:
                    for dungeon_ID in self.activeDungeonHandler.active_dungeon_ids:
                        dungeon_data = DungeonData(dungeon_id=dungeon_ID).load_data(dungeon_id=dungeon_ID)
                        dungeon_dict = {"dungeonID": dungeon_data.dungeon_id,
                                        "dungeonMasterID": dungeon_data.dungeon_master_id,
                                        "dungeonName": dungeon_data.name,
                                        "dungeonDescription": dungeon_data.description,
                                        "maxPlayers": dungeon_data.max_players, "accessList": dungeon_data.access_list,
                                        "private": dungeon_data.private}
                        dungeon_data_list.append(dungeon_dict)
                        print(colored(dungeon_dict, 'green'))
                    self.sio.emit('make_dungeon_available', json.dumps(dungeon_data_list), broadcast=True)
                    print(colored("publish successful", 'green'))
                else:
                    self.sio.emit('make_dungeon_available', json.dumps([]), broadcast=True)
            print('disconnect: ', sid)

        @self.sio.event
        def message(sid, data):
            print('message: ', data)
            self.sio.emit('message')

        @self.sio.event
        def on_leave_dungeon(sid, data):
            raise NotImplementedError
            # characterdaten speichern (mit room )
            # lobby avDungeons refreshen
            # in dungeon -> players -1

        @self.sio.event
        def send_character_config(sid, character):
            session = self.sio.get_session(sid)
            #TODO: inventory (class startitem)
            character_obj = Character(life_points=character["health"], name=character["name"], description=character["description"], class_id=character["class"]["classID"], race_id=character["race"]["raceID"], user_id=character["userID"], dungeon_id=character["dungeonID"])
            session["character"] = character_obj
            dungeon_manager = DungeonManager()
            dungeon_manager.write_character_to_database(character_obj)

        @self.sio.event
        def join_dungeon(sid, data):  # Data = Dict aus DungeonID und UserID/Name
            print("####", sid)
            session = self.sio.get_session(sid)
            user_status = self.access_manager.user_status_on_access_list(data['dungeonID'], session['userName'])
            if user_status:
                self.sio.enter_room(sid, data['dungeonID'])
                session['dungeonID'] = data['dungeonID']
                self.sio.emit('user_joined', f"'{session['userName']}' joined")
            elif user_status is False:
                print("wat isn jetzt passiert")
                self.sio.emit("on_join_request_answer", json.dumps(False), to=sid)
            elif not user_status:
                # TODO: Jack reden: Dungeon master anzeigen (toast)
                print("User will joinen:", sid)
                self.sio.emit('JoinRequest', json.dumps([data['userID'], session['userName']]),
                              to=self.activeDungeonHandler.sid_of_dungeon_master[data['dungeonID']])

            # übermittelt klassen & rassen

        @self.sio.event
        def create_character(sid, data):
            session = self.sio.get_session(sid)
            character = Character(user_id=session['userID'], name=data['name'], description=data['description'],
                                  class_id=data['classID'], race_id=data['raceID'], room_id=data['roomID'],
                                  dungeon_id=session['dungeonID'], character_id=str(uuid.uuid4()))
            session['characterID'] = character.character_id
            self.dungeon_manager.write_character_to_database(character)

        @self.sio.event
        def publish(sid, data):
            self.sio.enter_room(sid, data)
            self.activeDungeonHandler.dungeon_join(data)
            self.activeDungeonHandler.sid_of_dungeon_master[data] = sid
            session = self.sio.get_session(sid)
            session["dungeonID"] = data
            #########################

            dungeon_data_list = []
            for dungeon_ID in self.activeDungeonHandler.active_dungeon_ids:
                dungeon_data = DungeonData(dungeon_id=dungeon_ID).load_data(dungeon_id=dungeon_ID)
                dungeon_dict = {"dungeonID": dungeon_data.dungeon_id, "dungeonMasterID": dungeon_data.dungeon_master_id,
                                "dungeonName": dungeon_data.name, "dungeonDescription": dungeon_data.description,
                                "maxPlayers": dungeon_data.max_players, "accessList": dungeon_data.access_list,
                                "private": dungeon_data.private}
                dungeon_data_list.append(dungeon_dict)
                print(colored(dungeon_dict, 'green'))
            if len(dungeon_data_list) != 0:
                self.sio.emit('make_dungeon_available', json.dumps(dungeon_data_list), broadcast=True, skip_sid=sid)
                print(colored("publish successful", 'green'))

        # TODO: ausprobieren JACK!!!
        @self.sio.event
        def get_character_in_dungeon(sid, data):
            session = self.sio.get_session(sid)
            print("kleiner Test am Rande:", session)
            print(session["userID"], data["dungeonID"])
            character = Character().load_data(session["userID"], data["dungeonID"])
            print("Character: ")
            print(character)
            if character:
                self.sio.emit("get_character_in_dungeon", json.dumps(character.__dict__), to=sid)
            else:
                self.sio.emit("get_character_in_dungeon", json.dumps(False), to=sid)

        @self.sio.event
        def get_character_config(sid, data):
            json_obj = json.dumps(self.dungeon_manager.get_character_config(data))
            print("get charracter: ", json_obj)
            self.sio.emit('get_character_config', json_obj, sid)

        @self.sio.event
        def get_classes(sid, data):
            json_obj = json.dumps(self.dungeon_manager.get_all_from_classes_as_json(data))
            print("get classses: ", json_obj)
            self.sio.emit('classesData', json_obj, sid)

        @self.sio.event
        def get_races(sid, data):
            json_obj = json.dumps(self.dungeon_manager.get_all_from_races_as_json(data))
            print("get racces: ", json_obj)
            self.sio.emit('racesData', json_obj, sid)

        @self.sio.event
        def change_dungeonmaster(sid, data):
            session = self.sio.get_session()
            self.sio.emit("make_dungeonmaster", None, to=data['userID'])
