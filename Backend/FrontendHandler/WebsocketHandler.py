import json
import uuid

from termcolor import colored
from json import JSONEncoder
from BackendServices.AccessManager import AccessManager
from BackendServices.DungeonManager import DungeonManager
from DungeonPackage.ActiveDungeon import ActiveDungeon
from DungeonPackage.DungeonData import DungeonData
from DungeonPackage.Character import Character
from DungeonDirector.ActiveDungeonHandler import ActiveDungeonHandler
import socketio
import random


# TODO: user access management


class SocketIOHandler:
    def __init__(self):
        self.sio = socketio.Server(cors_allowed_origins='*', async_mode='eventlet', client_manager=socketio.BaseManager())
        self.sio.logger.disabled = True
        self.app = socketio.WSGIApp(self.sio)
        self.activeDungeonHandler = ActiveDungeonHandler()
        self.dungeon_manager = DungeonManager()
        self.access_manager = AccessManager()

        @self.sio.event
        def send_join_request_answer(sid, data):
            answer = data["isAllowed"]
            session = self.sio.get_session(self.activeDungeonHandler.user_sid[data['userID']])
            for socket in self.activeDungeonHandler.user_sid[data['userID']]:
                self.sio.emit("on_join_request_answer", answer, to=socket)
            count = self.activeDungeonHandler.user_count_in_dungeon[session['dungeonID']]
            self.activeDungeonHandler.user_count_in_dungeon[session['dungeonID']] = count + 1
            #region UpdateDungeon
            dungeon_data_list = []
            for dungeon_ID in self.activeDungeonHandler.active_dungeon_ids:
                dungeon_data = DungeonData(dungeon_id=dungeon_ID).load_data(dungeon_id=dungeon_ID)
                dungeon_dict = {"dungeonID": dungeon_data.dungeon_id,
                                "dungeonMasterID": dungeon_data.dungeon_master_id,
                                "dungeonName": dungeon_data.name,
                                "dungeonDescription": dungeon_data.description,
                                "maxPlayers": dungeon_data.max_players, "accessList": dungeon_data.access_list,
                                "private": dungeon_data.private,
                                "currentPlayers": self.activeDungeonHandler.user_count_in_dungeon[dungeon_ID]}
                dungeon_data_list.append(dungeon_dict)
                print(colored(dungeon_dict, 'green'))
            self.sio.emit('make_dungeon_available', json.dumps(dungeon_data_list), broadcast=True)
            #endregion

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
            #region UpdateDungeon
            dungeon_data_list = []

            for dungeon_ID in self.activeDungeonHandler.active_dungeon_ids:
                if self.activeDungeonHandler.sid_of_dungeon_master[dungeon_ID] != sid:

                    dungeon_data = DungeonData(dungeon_id=dungeon_ID).load_data(dungeon_id=dungeon_ID)

                    dungeon_dict = {"dungeonID": dungeon_data.dungeon_id,
                                    "dungeonMasterID": dungeon_data.dungeon_master_id,
                                    "dungeonName": dungeon_data.name, "dungeonDescription": dungeon_data.description,
                                    "maxPlayers": dungeon_data.max_players, "accessList": dungeon_data.access_list,
                                    "private": dungeon_data.private,
                                    "currentPlayers": self.activeDungeonHandler.user_count_in_dungeon[dungeon_ID]}

                    # len(self.sio.manager.get_participants(namespace="main", room=dungeon_data.dungeon_id))
                    dungeon_data_list.append(dungeon_dict)
                    print(colored(dungeon_dict, 'green'))
            self.sio.emit('make_dungeon_available', json.dumps(dungeon_data_list), to=sid)
            print(colored("publish successful", 'green'))
            #endregion

        @self.sio.event
        def connect(sid, environ, data):

            dungeon_data_list = []
            print(colored(f"Dungeon Data List: {dungeon_data_list}", 'red'))
            print(colored(f"Dungeon Handler List: {self.activeDungeonHandler.active_dungeon_ids}", 'red'))
            #region UpdateDungeon
            for dungeon_ID in self.activeDungeonHandler.active_dungeon_ids:
                if self.activeDungeonHandler.sid_of_dungeon_master[dungeon_ID] != sid:
                    dungeon_data = DungeonData(dungeon_id=dungeon_ID).load_data(dungeon_id=dungeon_ID)
                    dungeon_dict = {"dungeonID": dungeon_data.dungeon_id,
                                    "dungeonMasterID": dungeon_data.dungeon_master_id,
                                    "dungeonName": dungeon_data.name, "dungeonDescription": dungeon_data.description,
                                    "maxPlayers": dungeon_data.max_players, "accessList": dungeon_data.access_list,
                                    "private": dungeon_data.private,
                                    "currentPlayers": self.activeDungeonHandler.user_count_in_dungeon[dungeon_ID]}
                    dungeon_data_list.append(dungeon_dict)
                    print(colored(dungeon_dict, 'green'))
            if len(dungeon_data_list) != 0:
                self.sio.emit('make_dungeon_available', json.dumps(dungeon_data_list), broadcast=True)
                print(colored("publish successful", 'green'))
            #endregion

        # TODO: mit jack klären, dass aktive dungeons die vom dungeonmaster verlassen wurden beim dungeon master als
        # aktiv gekennzeicnet werden und dungeon ein beenden button bekommen
        @self.sio.event
        def disconnect(sid):
            # self.sio.leave_room(sid, self.sio.get_session(sid)['dungeonID'])

            if sid in self.activeDungeonHandler.sid_of_dungeon_master.values():
                dungeon_data_list = []
                self.activeDungeonHandler.dungeon_leave(self.sio.get_session(sid)['dungeonID'])
                #region UpdateDungeon
                if self.activeDungeonHandler.active_dungeon_ids.__len__() != 0:
                    for dungeon_ID in self.activeDungeonHandler.active_dungeon_ids:
                        dungeon_data = DungeonData(dungeon_id=dungeon_ID).load_data(dungeon_id=dungeon_ID)
                        dungeon_dict = {"dungeonID": dungeon_data.dungeon_id,
                                        "dungeonMasterID": dungeon_data.dungeon_master_id,
                                        "dungeonName": dungeon_data.name,
                                        "dungeonDescription": dungeon_data.description,
                                        "maxPlayers": dungeon_data.max_players, "accessList": dungeon_data.access_list,
                                        "private": dungeon_data.private,
                                        "currentPlayers": self.activeDungeonHandler.user_count_in_dungeon[dungeon_ID]}
                        dungeon_data_list.append(dungeon_dict)
                        print(colored(dungeon_dict, 'green'))
                    self.sio.emit('make_dungeon_available', json.dumps(dungeon_data_list), broadcast=True)
                    print(colored("publish successful", 'green'))
                else:
                    self.sio.emit('make_dungeon_available', json.dumps([]), broadcast=True)
                #endregion
            print('disconnect: ', sid)

            try:
                session = self.sio.get_session(sid)
                count = self.activeDungeonHandler.user_count_in_dungeon[session['dungeonID']]
                self.activeDungeonHandler.user_count_in_dungeon[session['dungeonID']] = count-+ 1
                dungeon_data_list = []
                #region UpdateDungeon
                for dungeon_ID in self.activeDungeonHandler.active_dungeon_ids:
                    dungeon_data = DungeonData(dungeon_id=dungeon_ID).load_data(dungeon_id=dungeon_ID)
                    dungeon_dict = {"dungeonID": dungeon_data.dungeon_id,
                                    "dungeonMasterID": dungeon_data.dungeon_master_id,
                                    "dungeonName": dungeon_data.name,
                                    "dungeonDescription": dungeon_data.description,
                                    "maxPlayers": dungeon_data.max_players, "accessList": dungeon_data.access_list,
                                    "private": dungeon_data.private,
                                    "currentPlayers": self.activeDungeonHandler.user_count_in_dungeon[dungeon_ID]}
                    dungeon_data_list.append(dungeon_dict)
                    print(colored(dungeon_dict, 'green'))
                self.sio.emit('make_dungeon_available', json.dumps(dungeon_data_list), broadcast=True)
                #endregion
            except:
                pass

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
            dungeon_id = character["dungeonID"]

            #region Adding user to starting room in active dungeon
            all_start_rooms = self.dungeon_manager.get_start_rooms_in_dungeon(dungeon_id=dungeon_id)
            starting_room = random.choice(all_start_rooms)
            #endregion

            #region Adding user to starting room in backend
            current_dungeon = ActiveDungeon(
                self.activeDungeonHandler.active_dungeons[dungeon_id]['active_dungeon_object'])
            current_dungeon.load_rooms(dungeon_id)
            all_rooms_in_dungeon = current_dungeon.rooms
            all_room_objects_in_dungeon = current_dungeon.rooms_objects
            for room in all_room_objects_in_dungeon[1:]:
                print(room)
                if room.room_id == starting_room['roomID']:
                    room.user_ids.append(character["userID"])
            #endregion

            session = self.sio.get_session(sid)
            # TODO: inventory (class startitem)
            character_obj = Character(room_id=starting_room['roomID'], life_points=character["health"],
                                      name=character["name"], description=character["description"],
                                      class_id=character["class"]["classID"], race_id=character["race"]["raceID"],
                                      user_id=character["userID"], dungeon_id=dungeon_id, character_id=str(uuid.uuid4()))
            session["character"] = character_obj
            self.dungeon_manager.write_character_to_database(character_obj)


            #region Adding class startitem to user inventory when first joining
            item = self.dungeon_manager.get_item_by_class_id(character["class"]["classID"])
            character_obj.add_item_to_inventory(item.item_id)
            #endregion

            self.sio.emit('character_joined_room',
                          json.dumps({'startRoom': starting_room, 'allOtherRoomsToLoad': all_rooms_in_dungeon}), sid=sid)

        @ self.sio.event
        def join_dungeon(sid, data):  # Data = Dict aus DungeonID und UserID/Name
            self.sio.enter_room(sid, data['dungeonID'])
            session = self.sio.get_session(sid)
            user_status = self.access_manager.user_status_on_access_list(data['dungeonID'], session['userName'])
            session['dungeonID'] = data['dungeonID']
            if user_status:
                self.sio.enter_room(sid, data['dungeonID'])
                count = self.activeDungeonHandler.user_count_in_dungeon[data['dungeonID']]
                self.activeDungeonHandler.user_count_in_dungeon[data['dungeonID']] = count + 1
                dungeon_data_list = []
                #region UpdateDungeon
                for dungeon_ID in self.activeDungeonHandler.active_dungeon_ids:
                    dungeon_data = DungeonData(dungeon_id=dungeon_ID).load_data(dungeon_id=dungeon_ID)
                    dungeon_dict = {"dungeonID": dungeon_data.dungeon_id,
                                    "dungeonMasterID": dungeon_data.dungeon_master_id,
                                    "dungeonName": dungeon_data.name,
                                    "dungeonDescription": dungeon_data.description,
                                    "maxPlayers": dungeon_data.max_players, "accessList": dungeon_data.access_list,
                                    "private": dungeon_data.private,
                                    "currentPlayers": self.activeDungeonHandler.user_count_in_dungeon[dungeon_ID]}
                    dungeon_data_list.append(dungeon_dict)
                    print(colored(dungeon_dict, 'green'))
                self.sio.emit('make_dungeon_available', json.dumps(dungeon_data_list), broadcast=True)
                self.sio.emit("on_join_request_answer", json.dumps(True), to=sid)
                #endregion
            elif user_status is False:
                print("wat isn jetzt passiert")
                self.sio.emit("on_join_request_answer", json.dumps(False), to=sid)
            elif not user_status:
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
            self.activeDungeonHandler.user_count_in_dungeon[data] = 0
            #########################
            #region UpdateDungeon
            dungeon_data_list = []
            for dungeon_ID in self.activeDungeonHandler.active_dungeon_ids:
                dungeon_data = DungeonData(dungeon_id=dungeon_ID).load_data(dungeon_id=dungeon_ID)
                dungeon_dict = {"dungeonID": dungeon_data.dungeon_id, "dungeonMasterID": dungeon_data.dungeon_master_id,
                                "dungeonName": dungeon_data.name, "dungeonDescription": dungeon_data.description,
                                "maxPlayers": dungeon_data.max_players, "accessList": dungeon_data.access_list,
                                "private": dungeon_data.private, "currentPlayers": 0}
                dungeon_data_list.append(dungeon_dict)
                print(colored(dungeon_dict, 'green'))
            if len(dungeon_data_list) != 0:
                self.sio.emit('make_dungeon_available', json.dumps(dungeon_data_list), broadcast=True, skip_sid=sid)
                print(colored("publish successful", 'green'))
            #endregion

        # TODO: ausprobieren JACK!!!
        @self.sio.event
        def get_character_in_dungeon(sid, data):
            session = self.sio.get_session(sid)
            print(session["userID"], data["dungeonID"])
            character = Character().load_data(session["userID"], data["dungeonID"])
            print("IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIICH")
            if character:
                print("HAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAB")
                print(character.to_dict())
                self.sio.emit("get_character_in_dungeon", json.dumps(character.to_dict()), to=sid)
            else:
                print("Kein bock :)")
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
