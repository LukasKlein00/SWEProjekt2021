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
import logging
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
from DungeonPackage.Item import Item
import socketio
import random

# TODO: user access management
from DungeonPackage.Inventory import Inventory
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
                                "currentPlayers": sum(1 for e in self.sio.manager.rooms['/'][dungeon_ID])}
                dungeon_data_list.append(dungeon_dict)
            self.sio.emit('make_dungeon_available', json.dumps(dungeon_data_list), broadcast=True)
            # endregion

        @self.sio.event
        def on_login(sid, data):

            self.sio.save_session(sid, {'userID': data['userID'], 'userName': data['username']})
            self.activeDungeonHandler.user_sid[data['userID']] = []
            self.activeDungeonHandler.user_sid_username[data['username']] = []
            array = self.activeDungeonHandler.user_sid[data['userID']]
            usernamearr = self.activeDungeonHandler.user_sid_username[data['username']]
            array.append(sid)
            usernamearr.append(sid)
            self.activeDungeonHandler.user_sid[data['userID']] = array
            self.activeDungeonHandler.user_sid_username[data['username']] = usernamearr

        @self.sio.event
        def on_home(sid):
            # region UpdateDungeon
            dungeon_data_list = []

            for dungeon_ID in self.activeDungeonHandler.active_dungeon_ids:
                print("help me pls", sum(1 for e in self.sio.manager.rooms['/'][dungeon_ID]))
                if self.activeDungeonHandler.sid_of_dungeon_master[dungeon_ID] != sid:
                    dungeon_data = DungeonData(dungeon_id=dungeon_ID).load_data(dungeon_id=dungeon_ID)

                    dungeon_dict = {"dungeonID": dungeon_data.dungeon_id,
                                    "dungeonMasterID": dungeon_data.dungeon_master_id,
                                    "dungeonName": dungeon_data.name, "dungeonDescription": dungeon_data.description,
                                    "maxPlayers": dungeon_data.max_players, "accessList": dungeon_data.access_list,
                                    "private": dungeon_data.private,
                                    "currentPlayers": sum(1 for e in self.sio.manager.rooms['/'][dungeon_ID])}


                    # len(self.sio.manager.get_participants(namespace="main", room=dungeon_data.dungeon_id))
                    dungeon_data_list.append(dungeon_dict)
            self.sio.emit('make_dungeon_available', json.dumps(dungeon_data_list), to=sid)
            # endregion

        @self.sio.event
        def connect(sid, environ, data):

            dungeon_data_list = []
            # region UpdateDungeon
            for dungeon_ID in self.activeDungeonHandler.active_dungeon_ids:
                if self.activeDungeonHandler.sid_of_dungeon_master[dungeon_ID] != sid:
                    dungeon_data = DungeonData(dungeon_id=dungeon_ID).load_data(dungeon_id=dungeon_ID)
                    dungeon_dict = {"dungeonID": dungeon_data.dungeon_id,
                                    "dungeonMasterID": dungeon_data.dungeon_master_id,
                                    "dungeonName": dungeon_data.name, "dungeonDescription": dungeon_data.description,
                                    "maxPlayers": dungeon_data.max_players, "accessList": dungeon_data.access_list,
                                    "private": dungeon_data.private,
                                    "currentPlayers": sum(1 for e in self.sio.manager.rooms['/'][dungeon_ID])}

                    dungeon_data_list.append(dungeon_dict)
            if len(dungeon_data_list) != 0:
                self.sio.emit('players_in_my_dungeon', json.dumps(
                    sum(1 for e in self.sio.manager.rooms['/'][dungeon_ID])), room=dungeon_ID)
                self.sio.emit('make_dungeon_available', json.dumps(dungeon_data_list), broadcast=True)
            # endregion

        # TODO: mit jack klären, dass aktive dungeons die vom dungeonmaster verlassen wurden beim dungeon master als
        # aktiv gekennzeicnet werden und dungeon ein beenden button bekommen

        @self.sio.event
        def disconnect(sid):
            # self.sio.leave_room(sid, self.sio.get_session(sid)['dungeonID'])

            if sid in self.activeDungeonHandler.sid_of_dungeon_master.values():
                dungeon_id = self.sio.get_session(sid)['dungeonID']

                self.activeDungeonHandler.active_dungeons_for_reconnect[dungeon_id] = False
                self.sio.emit('dungeon_is_active', json.dumps(False), room=dungeon_id)
                print('emitted dungeon_master_disconnected to :', dungeon_id)
                self.activeDungeonHandler.dungeon_leave(dungeon_id)
                # region UpdateDungeon

                dungeon_data_list = []
                if self.activeDungeonHandler.active_dungeon_ids.__len__() != 0:
                    for dungeon_ID in self.activeDungeonHandler.active_dungeon_ids:
                        dungeon_data = DungeonData(dungeon_id=dungeon_ID).load_data(dungeon_id=dungeon_ID)
                        dungeon_dict = {"dungeonID": dungeon_data.dungeon_id,
                                        "dungeonMasterID": dungeon_data.dungeon_master_id,
                                        "dungeonName": dungeon_data.name,
                                        "dungeonDescription": dungeon_data.description,
                                        "maxPlayers": dungeon_data.max_players, "accessList": dungeon_data.access_list,
                                        "private": dungeon_data.private,
                                        "currentPlayers": sum(1 for e in self.sio.manager.rooms['/'][dungeon_ID])}
                        dungeon_data_list.append(dungeon_dict)

                    self.sio.emit('make_dungeon_available', json.dumps(dungeon_data_list), broadcast=True)
                else:
                    self.sio.emit('make_dungeon_available', json.dumps([]), broadcast=True)
                    # self.sio.emit('players_in_my_dungeon', json.dumps(
                    #     sum(1 for e in self.sio.manager.rooms['/'][dungeon_ID])), room=dungeon_ID)
                # endregion

            try:
                session = self.sio.get_session(sid)
                if 'dungeonID' in session:
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
                                    "currentPlayers": sum(1 for e in self.sio.manager.rooms['/'][dungeon_ID])}
                    dungeon_data_list.append(dungeon_dict)
                self.sio.emit('make_dungeon_available', json.dumps(dungeon_data_list), broadcast=True)
                # self.sio.emit('players_in_my_dungeon', json.dumps(
                #     sum(1 for e in self.sio.manager.rooms['/'][dungeon_ID])), room=dungeon_ID)
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
            all_room_objects_in_dungeon = current_dungeon.rooms_objects

            session = self.sio.get_session(sid)
            # TODO: inventory (class startitem)
            character_obj = Character(room_id=starting_room['roomID'], life_points=character["health"],
                                      name=character["name"], description=character["description"],
                                      class_obj=Class(class_id=character["class"]["classID"]),
                                      race=Race(race_id=character["race"]["raceID"]),
                                      user_id=character["userID"],
                                      inventory=Inventory(dungeon_id=character['dungeonID'],
                                                          user_id=character['userID']),
                                      dungeon_id=dungeon_id,
                                      character_id=str(uuid.uuid4()))

            for room in all_room_objects_in_dungeon:
                if room.room_id == starting_room['roomID']:
                    room.user_ids.append(character["userID"])
                    character_obj.room_id = room.room_id
                    character_obj.discovered_rooms.append(room.room_id)
                    self.dungeon_manager.write_character_to_database(character_obj)
                    character_obj.discovered_rooms_to_database()
                    self.sio.enter_room(sid, room.room_id)
            self.sio.emit('current_room', json.dumps(starting_room), to=sid)
            try:
                discovered_rooms = []
                discovered_rooms.append(starting_room)
                session['discovered_rooms'] = discovered_rooms
                self.sio.emit('character_joined_room', json.dumps(discovered_rooms), to=sid)
            except:
                print("ohh ohh")
            # endregion

            item = self.dungeon_manager.get_item_by_class_id(character["class"]["classID"])
            try:
                character_obj.inventory.add_item_to_inventory(item.item_id)
            except AttributeError:
                print("Da war das item wohl none ¯\_(ツ)_/¯")
                pass

            session['character'] = character_obj
            self.sio.emit("get_character_in_dungeon", json.dumps(character_obj.to_dict()), to=sid)

        @self.sio.event
        def character_joined_room(sid, data):
            try:
                session = self.sio.get_session(sid)
                character = session['character']
                character.load_discovered_rooms_from_database()
                # region adding sid into dungeon
                temp_list = []
                if not character.dungeon_id in self.activeDungeonHandler.user_sids_in_dungeon:
                    temp_list.append(sid)
                    self.activeDungeonHandler.user_sids_in_dungeon[character.dungeon_id] = temp_list
                else:
                    temp_list = self.activeDungeonHandler.user_sids_in_dungeon[character.dungeon_id]
                    temp_list.append(sid)
                    self.activeDungeonHandler.user_sids_in_dungeon[character.dungeon_id] = temp_list
                # endregion
                all_discovered_rooms_ids_by_character = character.discovered_rooms
                all_discovered_rooms = self.dungeon_manager.get_data_for_room_list(
                    all_discovered_rooms_ids_by_character,
                    character.dungeon_id)
                session['discovered_rooms'] = all_discovered_rooms

                # fügt die aktuellen Spieler dem Current Room hinzu
                room = self.dungeon_manager.get_data_for_room_list(dungeon_id=character.dungeon_id, room_ids=[character.
                                                                   room_id])[0]

                playersSIDList = self.sio.manager.rooms['/'][character.room_id]
                players = []
                for player in playersSIDList:
                    myChar = self.sio.get_session(player)['character']
                    myCharDic = myChar.to_dict()
                    players.append(myCharDic)
                room['players'] = players
                self.sio.emit('current_room', json.dumps(room), room=character.room_id)

                self.sio.emit('character_joined_room', json.dumps(all_discovered_rooms), sid)
                self.sio.emit('current_room', json.dumps(room), room=character.room_id)
            except KeyError:
                logging.error("Character couldn't be loaded first time")

        @self.sio.event
        def join_dungeon(sid, data):  # Data = Dict aus DungeonID und UserID/Name
            # self.sio.enter_room(sid, data['dungeonID'])
            session = self.sio.get_session(sid)
            user_status = self.access_manager.user_status_on_access_list(data['dungeonID'], session['userName'])
            session['dungeonID'] = data['dungeonID']
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
                                    "currentPlayers": sum(1 for e in self.sio.manager.rooms['/'][dungeon_ID])}
                    dungeon_data_list.append(dungeon_dict)
                self.sio.emit('players_in_my_dungeon', json.dumps(
                    sum(1 for e in self.sio.manager.rooms['/'][dungeon_ID])), room=dungeon_ID)
                self.sio.emit('make_dungeon_available', json.dumps(dungeon_data_list), broadcast=True)
                self.sio.emit("on_join_request_answer", json.dumps(True), to=sid)
                # endregion
            elif user_status is False:
                self.sio.emit("on_join_request_answer", json.dumps(False), to=sid)
            elif not user_status:

                count = self.activeDungeonHandler.user_count_in_dungeon[data['dungeonID']]
                self.activeDungeonHandler.user_count_in_dungeon[data['dungeonID']] = count + 1
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
            session['character'] = character
            self.dungeon_manager.write_character_to_database(character)

        @self.sio.event
        def publish(sid, data):
            self.sio.enter_room(sid, data)

            if data in self.activeDungeonHandler.active_dungeons_for_reconnect:
                if not self.activeDungeonHandler.active_dungeons_for_reconnect[data]:
                    self.activeDungeonHandler.active_dungeons_for_reconnect[data] = True
                    self.sio.emit('dungeon_is_active', json.dumps(True), room=data)
                    print('emitted dungeon_is_active to', data)
            else:
                self.activeDungeonHandler.active_dungeons_for_reconnect[data] = True

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
                                "private": dungeon_data.private,
                                "currentPlayers": sum(1 for e in self.sio.manager.rooms['/'][dungeon_ID])}
                dungeon_data_list.append(dungeon_dict)
            if len(dungeon_data_list) != 0:
                self.sio.emit('make_dungeon_available', json.dumps(dungeon_data_list), broadcast=True, skip_sid=sid)
                self.sio.emit('players_in_my_dungeon', json.dumps(
                    sum(1 for e in self.sio.manager.rooms['/'][dungeon_ID])), room=dungeon_ID)
            # endregion

        # TODO: ausprobieren JACK!!!
        @self.sio.event
        def get_character_in_dungeon(sid, data):
            session = self.sio.get_session(sid)
            character = Character().load_data(session["userID"], data["dungeonID"])
            if character:
                inventory = Inventory(dungeon_id=data['dungeonID'], user_id=session['userID']).get_inventory()
                character.inventory = inventory
                session['character'] = character
                self.sio.enter_room(sid, character.room_id)
                self.sio.enter_room(sid, data["dungeonID"])
                char_dict = character.to_dict()
                print(char_dict)
                self.sio.emit("get_character_in_dungeon", json.dumps(char_dict), to=sid)
            else:
                self.sio.emit("get_character_in_dungeon", json.dumps(False), to=sid)

        @self.sio.event
        def get_character_config(sid, data):
            json_obj = json.dumps(self.dungeon_manager.get_character_config(data['dungeonID']))
            self.sio.emit('get_character_config', json_obj, sid)

        @self.sio.event
        def get_classes(sid, data):
            json_obj = json.dumps(self.dungeon_manager.get_all_from_classes_as_json(data))
            self.sio.emit('classesData', json_obj, sid)

        @self.sio.event
        def get_races(sid, data):
            json_obj = json.dumps(self.dungeon_manager.get_all_from_races_as_json(data))
            self.sio.emit('racesData', json_obj, sid)

        # @self.sio.event
        # def change_dungeonmaster(sid, data):
        #     session = self.sio.get_session()
        #     self.sio.emit("make_dungeonmaster", None, to=data['userID'])

        @self.sio.event
        def move_to_room(sid, data):
            # data = {dungeonID, userID, direction}
            # TODO: (self.sio.leave_room(sid, oldroom.room_id)
            #       self.sio.enter_room(sid, newroom.room_id)
            session = self.sio.get_session(sid)
            character = session['character']
            discovered_rooms = session['discovered_rooms']
            discovered_room_ids = list(map(lambda x: x['roomID'], discovered_rooms))
            current_room = character.room_id  # None

            current_dungeon = ActiveDungeon(
                self.activeDungeonHandler.active_dungeons[data['dungeonID']]['active_dungeon_object'])

            current_dungeon.load_rooms(data['dungeonID'])

            try:
                for room in current_dungeon.room_dick_list:
                    if room['roomID'] == current_room:
                        room_data = room
                        y_coordinate = room_data['y']
                        x_coordinate = room_data['x']
                        pass

                if bool(room_data[data['direction']]) is True:
                    move_message = {'msg': f"moved {data['direction']}",
                                    'pre': "success:",
                                    'color': "#88B04B"
                                    }
                    # region North
                    if data['direction'] == 'north':
                        for room in current_dungeon.room_dick_list:
                            if x_coordinate == room['x'] and (y_coordinate - 1) == room['y']:
                                self.sio.leave_room(sid, character.room_id)
                                character.room_id = room['roomID']
                                self.sio.enter_room(sid, character.room_id)
                                already_discovered = False
                                for discovered_room in discovered_rooms:
                                    if room['roomID'] == discovered_room['roomID']:
                                        already_discovered = True
                                if already_discovered is False:
                                    discovered_rooms.append(room)
                                    discovered_room_ids.append(room['roomID'])
                                # fügt die aktuellen Spieler dem Current Room hinzu
                                playersSIDList = self.sio.manager.rooms['/'][character.room_id]
                                players = []
                                for player in playersSIDList:
                                    myChar = self.sio.get_session(player)['character']
                                    myCharDic = myChar.to_dict()
                                    players.append(myCharDic)
                                room['players'] = players
                                self.sio.emit('current_room', json.dumps(room), room=character.room_id)

                                try:
                                    # fügt die aktuellen Spieler dem Room hinzu, den er verlässt
                                    playersSIDList = self.sio.manager.rooms['/'][current_room]
                                    players = []
                                    for player in playersSIDList:
                                        myChar = self.sio.get_session(player)['character']
                                        myCharDic = myChar.to_dict()
                                        players.append(myCharDic)
                                    room_data['players'] = players
                                    self.sio.emit('current_room', json.dumps(room_data), room=current_room)
                                except:
                                    pass

                                character.discovered_rooms = discovered_room_ids
                                character.discovered_rooms_to_database()
                                character.update_current_room()
                                self.sio.emit('current_room', json.dumps(room), to=sid)
                                self.sio.emit('character_joined_room', json.dumps(discovered_rooms), to=sid)
                                self.sio.emit('get_chat', json.dumps(move_message), to=sid)
                                pass
                    # endregion
                    if data['direction'] == 'east':
                        for room in current_dungeon.room_dick_list:
                            if (x_coordinate + 1) == room['x'] and y_coordinate == room['y']:
                                self.sio.leave_room(sid, character.room_id)
                                character.room_id = room['roomID']
                                self.sio.enter_room(sid, character.room_id)
                                already_discovered = False
                                for discovered_room in discovered_rooms:
                                    if room['roomID'] == discovered_room['roomID']:
                                        already_discovered = True
                                if already_discovered is False:
                                    discovered_rooms.append(room)
                                    discovered_room_ids.append(room['roomID'])
                                # fügt die aktuellen Spieler dem Current Room hinzu
                                playersSIDList = self.sio.manager.rooms['/'][character.room_id]
                                players = []
                                for player in playersSIDList:
                                    myChar = self.sio.get_session(player)['character']
                                    myCharDic = myChar.to_dict()
                                    players.append(myCharDic)
                                room['players'] = players
                                self.sio.emit('current_room', json.dumps(room), room=character.room_id)

                                try:
                                    # fügt die aktuellen Spieler dem Room hinzu, den er verlässt
                                    playersSIDList = self.sio.manager.rooms['/'][current_room]
                                    players = []
                                    for player in playersSIDList:
                                        myChar = self.sio.get_session(player)['character']
                                        myCharDic = myChar.to_dict()
                                        players.append(myCharDic)
                                    room_data['players'] = players
                                    self.sio.emit('current_room', json.dumps(room_data), room=current_room)
                                except:
                                    pass

                                character.discovered_rooms = discovered_room_ids
                                character.discovered_rooms_to_database()
                                character.update_current_room()
                                self.sio.emit('current_room', json.dumps(room), to=sid)
                                self.sio.emit('character_joined_room', json.dumps(discovered_rooms), to=sid)
                                self.sio.emit('get_chat', json.dumps(move_message), to=sid)
                                pass
                    if data['direction'] == 'south':
                        for room in current_dungeon.room_dick_list:
                            if x_coordinate == room['x'] and (y_coordinate + 1) == room['y']:
                                self.sio.leave_room(sid, character.room_id)
                                character.room_id = room['roomID']
                                self.sio.enter_room(sid, character.room_id)
                                already_discovered = False
                                for discovered_room in discovered_rooms:
                                    if room['roomID'] == discovered_room['roomID']:
                                        already_discovered = True
                                if already_discovered is False:
                                    discovered_rooms.append(room)
                                    discovered_room_ids.append(room['roomID'])
                                # fügt die aktuellen Spieler dem Current Room hinzu
                                playersSIDList = self.sio.manager.rooms['/'][character.room_id]
                                players = []
                                for player in playersSIDList:
                                    myChar = self.sio.get_session(player)['character']
                                    myCharDic = myChar.to_dict()
                                    players.append(myCharDic)
                                room['players'] = players
                                self.sio.emit('current_room', json.dumps(room), room=character.room_id)

                                try:
                                    # fügt die aktuellen Spieler dem Room hinzu, den er verlässt
                                    playersSIDList = self.sio.manager.rooms['/'][current_room]
                                    players = []
                                    for player in playersSIDList:
                                        myChar = self.sio.get_session(player)['character']
                                        myCharDic = myChar.to_dict()
                                        players.append(myCharDic)
                                    room_data['players'] = players
                                    self.sio.emit('current_room', json.dumps(room_data), room=current_room)
                                except:
                                    pass

                                character.discovered_rooms = discovered_room_ids
                                character.discovered_rooms_to_database()
                                character.update_current_room()
                                self.sio.emit('current_room', json.dumps(room), to=sid)
                                self.sio.emit('character_joined_room', json.dumps(discovered_rooms), to=sid)
                                self.sio.emit('get_chat', json.dumps(move_message), to=sid)
                                pass
                    if data['direction'] == 'west':
                        for room in current_dungeon.room_dick_list:
                            if (x_coordinate - 1) == room['x'] and y_coordinate == room['y']:
                                self.sio.leave_room(sid, character.room_id)
                                character.room_id = room['roomID']
                                self.sio.enter_room(sid, character.room_id)
                                already_discovered = False
                                for discovered_room in discovered_rooms:
                                    if room['roomID'] == discovered_room['roomID']:
                                        already_discovered = True
                                if already_discovered is False:
                                    discovered_rooms.append(room)
                                    discovered_room_ids.append(room['roomID'])
                                # fügt die aktuellen Spieler dem Current Room hinzu
                                playersSIDList = self.sio.manager.rooms['/'][character.room_id]
                                players = []
                                for player in playersSIDList:
                                    myChar = self.sio.get_session(player)['character']
                                    myCharDic = myChar.to_dict()
                                    players.append(myCharDic)
                                room['players'] = players
                                self.sio.emit('current_room', json.dumps(room), room=character.room_id)

                                try:
                                    # fügt die aktuellen Spieler dem Room hinzu, den er verlässt
                                    playersSIDList = self.sio.manager.rooms['/'][current_room]
                                    players = []
                                    for player in playersSIDList:
                                        myChar = self.sio.get_session(player)['character']
                                        myCharDic = myChar.to_dict()
                                        players.append(myCharDic)
                                    room_data['players'] = players
                                    self.sio.emit('current_room', json.dumps(room_data), room=current_room)
                                except:
                                    pass

                                character.discovered_rooms = discovered_room_ids
                                character.discovered_rooms_to_database()
                                character.update_current_room()
                                self.sio.emit('current_room', json.dumps(room), to=sid)
                                self.sio.emit('character_joined_room', json.dumps(discovered_rooms), to=sid)
                                self.sio.emit('get_chat', json.dumps(move_message), to=sid)
                                pass
                else:
                    msg = {'msg': "couldn't move in this direction",
                           'pre': "error:",
                           'color': "#DD4124"
                           }

                    self.sio.emit('get_chat', json.dumps(msg), to=sid)

            except IOError:
                pass
            # ist Raum in gewünschte richtung offen?
            # ist da ein Raum?
            # if so -> move character id from roomID(alt) to roomID(neu)
            # geb zurück neue koordinaten für frontend

        @self.sio.event
        def dungeon_master_request(sid, data):
            session = self.sio.get_session(sid)
            character_object = session['character']
            room = self.dungeon_manager.load_room_coordinates(character_object.room_id)
            dungeon_master_sid = self.activeDungeonHandler.sid_of_dungeon_master[data['dungeonID']]
            request = {'userID': session['userID'], 'dungeonID': data['dungeonID'], 'request': data['message'],
                       'requester': character_object.to_dict(), 'answer': "", 'x': room['x'], 'y': room['y']}
            self.sio.emit("send_request_to_dm", json.dumps(request), to=dungeon_master_sid)

        @self.sio.event
        def send_message_to_master(sid, data):
            session = self.sio.get_session(sid)
            dungeon_master_sid = self.activeDungeonHandler.sid_of_dungeon_master[data['dungeonID']]
            msg = {'pre': session['character'].name + ':', 'msg': data['message']}
            user_msg = {'pre': "message to DM: ", 'msg': data['message']}
            self.sio.emit('get_chat', json.dumps(msg), to=dungeon_master_sid)
            self.sio.emit('get_chat', json.dumps(user_msg), to=sid)

        @self.sio.event
        def send_message_to_room(sid, data):
            session = self.sio.get_session(sid)
            character = session['character']
            room_to_send = character.room_id
            msg = {'pre': character.name + ": ", 'msg': data['message']}
            self.sio.emit('get_chat', json.dumps(msg), room=room_to_send)

        @self.sio.event
        def send_message_to_all(sid, data):
            msg = {'pre': ("DM: "), 'msg': data['message'], 'color': '#FF6F61'}
            self.sio.emit('get_chat', json.dumps(msg), room=data['dungeonID'])

        @self.sio.event
        def send_whisper_to_player(sid, data):
            receiver = re.search(r'".*"', data['message']).group()[1:-1]
            message = re.split(r'".*"', data['message'])[1]
            user_id_of_recipient = self.dungeon_manager.get_userid_by_character_name(receiver, data['dungeonID'])
            sid_of_recipient = self.activeDungeonHandler.user_sid[user_id_of_recipient]
            msg = {'pre': "DM whispered: ", 'msg': message, 'color': '#D65076'}
            dm_msg = {'pre': f"whispered to '{receiver}' :", 'msg': message}
            self.sio.emit('get_chat', json.dumps(msg), to=sid_of_recipient[0])
            self.sio.emit('get_chat', json.dumps(dm_msg), to=sid)

        @self.sio.event
        def send_whisper_to_room(sid, data):
            session = self.sio.get_session(sid)
            character = session['character']
            receiver = re.search(r'".*"', data['message']).group()[1:-1]
            message = re.split(r'".*"', data['message'])[1]
            user_id_of_recipient = self.dungeon_manager.get_userid_by_character_name(receiver, data['dungeonID'])
            try:
                sid_of_recipient = self.activeDungeonHandler.user_sid[user_id_of_recipient]
                if self.sio.rooms(sid_of_recipient[0]).__contains__(character.room_id):
                    msg = {'pre': character.name + " whispered: ", 'msg': message, 'color': '#D65076'}
                    self.sio.emit('get_chat', json.dumps(msg), room=character.room_id)
                else:
                    msg = {'pre': "error:",
                           'msg': "the character you're trying to message is not in the same room (•_•)",
                           'color': "#DD4124"}
                    self.sio.emit('get_chat', json.dumps(msg), to=sid)
            except KeyError:
                msg = {'pre': "error:", 'msg': "the character you're trying to message does not exist (•_•)",
                       'color': "#DD4124"}
                self.sio.emit('get_chat', json.dumps(msg), to=sid)

        @self.sio.event
        def dungeon_master_request_answer_to_user(sid,
                                                  data):  # data = dungeonID, userID, health, character with inventory
            new_health = data['requester']['health']
            sid_of_recipient = self.activeDungeonHandler.user_sid[data['requester']['userID']][0]
            session = self.sio.get_session(sid_of_recipient)
            character = session['character']

            if new_health == 0:
                print("health is zero")
                self.dungeon_manager.delete_discovered_rooms(data['userID'], data['dungeonID'])
                self.dungeon_manager.delete_inventory(data['userID'], data['dungeonID'])
                self.dungeon_manager.delete_character(data['userID'], data['dungeonID'])

                del session['character']
                self.sio.emit('kick_out', json.dumps(f"you died ._., response: '{data['answer']}'"), to=sid_of_recipient)

            else:
                received_character_inventory = data['requester']['inventory']
                print("received inventory", data['requester']['inventory'])
                inventory = Inventory(dungeon_id=data['dungeonID'],
                                      user_id=data['userID'])
                inventory.delete_inventory()
                for item in received_character_inventory:
                    print("okay lets go")
                    item_object = Item(item_id=item['itemID'], name=item['name'], description=item['description'])
                    inventory.add_item_to_inventory(item['itemID'], item_object)

                character.inventory = inventory
                print("health is not zero")
                msg = {'msg': data['answer'], 'color': '#FF6F61', 'dmRequest': True, 'pre': 'consequence:'}
                character.life_points = new_health
                self.sio.emit("get_character_in_dungeon", json.dumps(character.to_dict()), to=sid_of_recipient)
                self.sio.emit('get_chat', json.dumps(msg), to=sid_of_recipient)

        @self.sio.event
        def delete_dungeon(sid, data):  # data = dungeonID
            for user_sid in self.activeDungeonHandler.user_sids_in_dungeon[data['dungeonID']]:
                self.sio.emit('kick_out', json.dumps("The Dungeon you were playing in was deleted", to=user_sid))
            self.dungeon_manager.delete_dungeon(data['dungeonID'])
