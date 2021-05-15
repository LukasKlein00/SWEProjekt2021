#!/usr/bin/env python
__author__ = "Jan Gruchott & Lukas Klein & Thomas Zimmermann"
__copyright__ = "Copyright 2021, The MUDCake Project"
__credits__ = "Hauke Presig, Jack Drillisch, Jan Gruchott, Lukas Klein, Robert Fendrich, Thomas Zimmermann"

__license__ = """MIT License

                     Copyright (c) 2021 MUDCake Project

                     Permission is hereby granted, free of charge, to any person obtaining a copy
                     of this software and associated documentation files (the "Software"), to deal
                     in the Software without restriction, including without limitation the rights
                     to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
                     copies of the Software, and to permit persons to whom the Software is
                     furnished to do so, subject to the following conditions:

                     The above copyright notice and this permission notice shall be included in all
                     copies or substantial portions of the Software.

                     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
                     IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
                     FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
                     AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
                     LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
                     OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
                     SOFTWARE."""

__version__ = "1.0.0"
__maintainer__ = "Jan Gruchott & Lukas Klein & Thomas Zimmermann"
__email__ = "mudcake@gmail.com"
__status__ = "Development"

import json
import random
import uuid
import re


import socketio
from termcolor import colored

from BackendServices.AccessManager import AccessManager
from BackendServices.DungeonManager import DungeonManager
from DungeonDirector.ActiveDungeonHandler import ActiveDungeonHandler
from DungeonPackage.ActiveDungeon import ActiveDungeon
from DungeonPackage.Character import Character
from DungeonPackage.Class import Class
from DungeonPackage.DungeonData import DungeonData
from DungeonPackage.Character import Character
from DungeonDirector.ActiveDungeonHandler import ActiveDungeonHandler
import socketio
import random

# TODO: user access management
from DungeonPackage.Race import Race


class SocketIOHandler:
    def __init__(self):
        self.sio = socketio.Server(cors_allowed_origins='*', async_mode='eventlet',
                                   client_manager=socketio.BaseManager())
        self.sio.logger.disabled = True
        self.app = socketio.WSGIApp(self.sio)
        self.activeDungeonHandler = ActiveDungeonHandler()
        self.dungeon_manager = DungeonManager()
        self.access_manager = AccessManager()

        @self.sio.event
        def move_to_room(sid, data):
            raise NotImplementedError

        @self.sio.event
        def dungeon_master_request(sid, data):
            raise NotImplementedError

        @self.sio.event
        def send_join_request_answer(sid, data):
            answer = data["isAllowed"]
            session = self.sio.get_session(self.activeDungeonHandler.user_sid[data['userID']][0])
            for socket in self.activeDungeonHandler.user_sid[data['userID']]:
                self.sio.emit("on_join_request_answer", answer, to=socket)
            count = self.activeDungeonHandler.user_count_in_dungeon[session['dungeonID']]
            self.activeDungeonHandler.user_count_in_dungeon[session['dungeonID']] = count + 1
            # region UpdateDungeon
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
            # endregion

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
            # region UpdateDungeon
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
            # endregion

        @self.sio.event
        def connect(sid, environ, data):

            dungeon_data_list = []
            print(colored(f"Dungeon Data List: {dungeon_data_list}", 'red'))
            print(colored(f"Dungeon Handler List: {self.activeDungeonHandler.active_dungeon_ids}", 'red'))
            # region UpdateDungeon
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
            # endregion

        # TODO: mit jack klären, dass aktive dungeons die vom dungeonmaster verlassen wurden beim dungeon master als
        # aktiv gekennzeicnet werden und dungeon ein beenden button bekommen

        @self.sio.event
        def disconnect(sid):
            # self.sio.leave_room(sid, self.sio.get_session(sid)['dungeonID'])

            if sid in self.activeDungeonHandler.sid_of_dungeon_master.values():
                dungeon_data_list = []
                self.activeDungeonHandler.dungeon_leave(self.sio.get_session(sid)['dungeonID'])
                # region UpdateDungeon
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
                # endregion
            print('disconnect: ', sid)

            try:
                session = self.sio.get_session(sid)
                count = self.activeDungeonHandler.user_count_in_dungeon[session['dungeonID']]
                self.activeDungeonHandler.user_count_in_dungeon[session['dungeonID']] = count - + 1
                dungeon_data_list = []
                # region UpdateDungeon
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
                # endregion
            except IOError:
                pass

        @self.sio.event
        def on_leave_dungeon(sid, data):
            raise NotImplementedError
            # characterdaten speichern (mit room )
            # lobby avDungeons refreshen
            # in dungeon -> players -1

        @self.sio.event
        def send_character_config(sid, character):
            dungeon_id = character["dungeonID"]

            # region Adding user to starting room in active dungeon
            all_start_rooms = self.dungeon_manager.get_start_rooms_in_dungeon(dungeon_id=dungeon_id)
            starting_room = random.choice(all_start_rooms)
            # endregion

            # region Adding user to starting room in backend
            current_dungeon = ActiveDungeon(
                self.activeDungeonHandler.active_dungeons[dungeon_id]['active_dungeon_object'])
            current_dungeon.load_rooms(dungeon_id)
            all_rooms_in_dungeon = current_dungeon.rooms
            all_room_objects_in_dungeon = current_dungeon.rooms_objects

            session = self.sio.get_session(sid)
            # TODO: inventory (class startitem)
            character_obj = Character(room_id=starting_room['roomID'], life_points=character["health"],
                                      name=character["name"], description=character["description"],
                                      class_obj=Class(class_id=character["class"]["classID"]),
                                      race=Race(race_id=character["race"]["raceID"]),
                                      user_id=character["userID"], dungeon_id=dungeon_id,
                                      character_id=str(uuid.uuid4()))
            session["character"] = character_obj

            for room in all_room_objects_in_dungeon[1:]:
                print(room)
                if room.room_id == starting_room['roomID']:
                    room.user_ids.append(character["userID"])
                    character = self.sio.get_session(sid)['character']
                    character.room_id = room.room_id
                    character.discovered_rooms.append(room.room_id)
                    character.discovered_rooms_to_database()
                    self.sio.enter_room(sid, room.room_id)
            # endregion

            self.dungeon_manager.write_character_to_database(character_obj)

            # region Adding class startitem to user inventory when first joining
            item = self.dungeon_manager.get_item_by_class_id(character["class"]["classID"])
            character_obj.add_item_to_inventory(item.item_id)
            # endregion

        @self.sio.event
        def character_joins_dungeon(sid, character):
            character_obj = Character(life_points=character["health"],
                                      name=character["name"], description=character["description"],
                                      user_id=character["userID"], dungeon_id=character['dungeonID'])
            character_obj.load_discovered_rooms_from_database()
            all_discovered_rooms_ids_by_character = character_obj.discovered_rooms
            all_discovered_rooms = self.dungeon_manager.get_data_for_room_list(all_discovered_rooms_ids_by_character,
                                                                               character['dungeonID'])
            self.sio.emit('character_joined_room', json.dumps(all_discovered_rooms), sid)

        @self.sio.event
        def join_dungeon(sid, data):  # Data = Dict aus DungeonID und UserID/Name
            self.sio.enter_room(sid, data['dungeonID'])
            session = self.sio.get_session(sid)
            user_status = self.access_manager.user_status_on_access_list(data['dungeonID'], session['userName'])
            session['dungeonID'] = data['dungeonID']
            print("User Status: ", user_status)
            if user_status:
                self.sio.enter_room(sid, data['dungeonID'])
                count = self.activeDungeonHandler.user_count_in_dungeon[data['dungeonID']]
                self.activeDungeonHandler.user_count_in_dungeon[data['dungeonID']] = count + 1
                dungeon_data_list = []
                # region UpdateDungeon
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
                # endregion
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
            # region UpdateDungeon
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
            # endregion

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
                self.sio.enter_room(sid, character.room_id)
                self.sio.emit("get_character_in_dungeon", json.dumps(character.to_dict()), to=sid)
            else:
                print("Kein bock :)")
                self.sio.emit("get_character_in_dungeon", json.dumps(False), to=sid)

        @self.sio.event
        def get_character_config(sid, data):
            json_obj = json.dumps(self.dungeon_manager.get_character_config(data['dungeonID']))
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

        @self.sio.event
        def move_to_room(sid, data):
            # data = {dungeonID, userID, direction}
            #TODO: (self.sio.leave_room(sid, oldroom.room_id)
            #       self.sio.enter_room(sid, newroom.room_id)
            character = self.sio.get_session(sid)['character']
            current_room = character.room_id

            current_dungeon = ActiveDungeon(
                self.activeDungeonHandler.active_dungeons(data['dungeon_id'])['active_dungeon_object'])

            room_data = next(room for room in current_dungeon.rooms if room["roomID"] == current_room)
            print(room_data)

            y_coordinate = room_data['y']
            x_coordinate = room_data['x']

            if room_data[data['direction']] is True:
                if data['direction'] == 'north':
                    for room in current_dungeon.rooms:
                        if x_coordinate == room['x'] and (y_coordinate + 1) == room['y']:
                            character.room_id = room['roomID']

                        else:
                            self.sio.emit('no_room_in_this_direction', json.dumps(False), to=sid)

            # ist Raum in gewünschte richtung offen?
            # ist da ein Raum?
            # if so -> move character id from roomID(alt) to roomID(neu)
            # geb zurück neue koordinaten für frontend
            raise NotImplementedError

        @self.sio.event
        def dungeon_master_request(sid, data):  # dungeonID, userID, message
            session = self.sio.get_session(sid)
            character_object = session['character']
            dungeon_master_sid = self.activeDungeonHandler.sid_of_dungeon_master[data['dungeonID']]
            request = {'userName': session['userName'], 'message': data['message'],
                       'character': character_object.to_dict()}
            self.sio.emit("send_request_to_dm", json.dumps(request), to=dungeon_master_sid)

        @self.sio.event
        def send_message_to_master(sid, data):
            print("send_message_to_master")
            session = self.sio.get_session(sid)
            dungeon_master_sid = self.activeDungeonHandler.sid_of_dungeon_master[data['dungeonID']]
            msg = {'pre': session['character'].name, 'msg': data['message']}
            self.sio.emit('get_chat', json.dumps(msg), to=dungeon_master_sid)

        @self.sio.event
        def send_message_to_room(sid, data):
            print("send_message_to_room")
            session = self.sio.get_session(sid)
            character = session['character']
            room_to_send = character.room_id
            msg = {'pre': character.name, 'msg': data['message']}
            self.sio.emit('get_chat', json.dumps(msg), room=room_to_send)

        @self.sio.event
        def send_message_to_all(sid, data):
            print("send_message_to_all")
            session = self.sio.get_session(sid)
            msg = {'pre': session['userName'], 'msg': data['message']}
            self.sio.emit('get_chat', json.dumps(msg), room=data['dungeonID'])

        #@self.sio.event
        #def send_whisper_to_player(sid, data):
        #    session = self.sio.get_session(sid)
        #    receiver = re.findall(r'".*"', data['msg'])[0][1:-1]
        #    for user_session in self.activeDungeonHandler.active_dungeons[data['dungeonID']]

