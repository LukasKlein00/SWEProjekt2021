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
from http.server import BaseHTTPRequestHandler

from BackendServices.AccountManager import AccountManager
from BackendServices.DungeonManager import DungeonManager


class HTTPHandler(BaseHTTPRequestHandler):

    acc_manager = AccountManager()
    dung_manager = DungeonManager()

    def log_message(self, format, *args):
        return

    # übermittelt Einstellungen "Headers" des Requests
    def __set_response(self, code: int = 200):
        self.send_response(code)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET')
        self.send_header('Access-Control-Allow-Headers', 'Authorization, Content-Type')
        self.end_headers()

    # OPTIONS Request: Wird vor jeder Request ausgeführt, um zu checken, ob die Request erlaubt ist
    def do_OPTIONS(self):
        self.__set_response()

        # GET Request: "Wird verwendet wenn Daten ausgegeben werden sollen"

    def do_GET(self):
        pass

    # POST Request: "Wird verwendet wenn Daten angenommen werden sollen"
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])  # <--- Größe der Daten
        post_data_raw = self.rfile.read(content_length)  # <--- Erfasst die Daten
        print(self.path)
        try:
            data = json.loads(post_data_raw)  # <--Daten als JSON-Objekt
            print('data', data)
        except:
            data = None

        if self.path == '/confirm':
            self.__set_response()
            try:
                self.acc_manager.confirm_registration_token(data['token'])
            except:
                print("/confirm received but error")
                pass

        if self.path == '/register':
            self.__set_response()
            print(self.path)
            try:
                self.acc_manager.register_user(user_id=data['userID'], first_name=data['firstName'], last_name=data['lastName'],
                                               user_name=data['username'], e_mail=data['email'], password=data['password'],
                                               is_confirmed=False)

                self.acc_manager.send_registration_email(data['email'], data['userID'])
            except:
                pass


        if self.path == '/login':
            self.__set_response()
            try:
                response = self.acc_manager.check_login_credentials(Username=data['username'], Password=data['password'])
                self.wfile.write(json.dumps(response).encode(encoding='utf_8'))
            except:
                self.__set_response(400)

        if self.path == '/getMyDungeons':
            self.__set_response()
            dungeon_manager = DungeonManager()
            dungeons = dungeon_manager.get_dungeon_by_id(data)
            self.wfile.write(json.dumps(dungeons).encode(encoding='utf_8'))

        if self.path == '/getDungeon':
            self.__set_response()
            dungeon_manager = DungeonManager()
            dungeon = dungeon_manager.get_dungeon_data_by_dungeon_id(data)
            self.wfile.write(json.dumps(dungeon).encode(encoding='utf_8'))

        if self.path == '/getRooms':
            self.__set_response()
            dungeon_manager = DungeonManager()
            rooms = dungeon_manager.get_all_from_room_as_json(data)
            rooms_json = json.dumps(rooms).encode(encoding='utf_8')
            print("rooms as json returned: " + str(rooms_json))
            self.wfile.write(rooms_json)

        if self.path == '/getRaces':
            self.__set_response()
            dungeon_manager = DungeonManager()
            races = json.dumps(dungeon_manager.get_all_from_races_as_json(data)).encode(encoding='utf_8')
            self.wfile.write(races)

        if self.path == '/getClasses':
            self.__set_response()
            dungeon_manager = DungeonManager()
            classes = json.dumps(dungeon_manager.get_all_from_classes_as_json(data)).encode(encoding='utf_8')
            self.wfile.write(classes)

        if self.path == '/getNpcs':
            self.__set_response()
            dungeon_manager = DungeonManager()
            rooms = dungeon_manager.get_all_from_npcs_as_json(data)
            self.wfile.write(rooms)

        if self.path == '/getItems':
            self.__set_response()
            dungeon_manager = DungeonManager()
            rooms = dungeon_manager.get_all_from_items_as_json(data)
            self.wfile.write(rooms)

        if self.path == '/getAccessList':
            self.__set_response()
            dungeon_manager = DungeonManager()
            access_list = dungeon_manager.get_accesslist(data)
            print(access_list)
            self.wfile.write(json.dumps(access_list).encode(encoding='utf_8'))
            print("acceslist sent")

        if self.path == '/deleteAccess':
            self.__set_response()
            print("this is the delete accesslist stuff yep yep")
            dungeon_manager = DungeonManager()
            dungeon_manager.delete_user_from_accesslist(data)


        if self.path == '/saveDungeon':
            self.__set_response()
            dungeon_manager = DungeonManager(data)
            dungeon_id = dungeon_manager.write_dungeon_to_database()
            try:
                print(json.dumps(dungeon_id).encode(encoding='utf_8'))
                self.wfile.write(json.dumps(dungeon_id).encode(encoding='utf_8'))
            except IOError:
                pass

        if self.path == '/deleteDungeon':
            self.__set_response()
            dungeon_manager = DungeonManager()
            dungeon_manager.delete_dungeon(data)

        if self.path == '/delete_user':
            self.__set_response()
            delete_transaction = self.acc_manager.delete_user(user_id=data)
            if not delete_transaction:
                self.__set_response(400)

        if self.path == '/copyDungeon':
            print(data)
            self.__set_response()
            dungeon_manager = DungeonManager()
            dungeon_manager.copy_dungeon(data)

        if self.path == '/forgot':
            self.__set_response()
            self.acc_manager.send_password_reset_email(user_email=data['email'])

        if self.path == '/reset':
            self.__set_response()
            print("data")
            print(data)
            is_password_changed = self.acc_manager.change_password_in_database(user_id=data['token'], password=data['password'])
            if not is_password_changed:
                self.__set_response(400)

        if self.path == '/check':
            self.__set_response()
            check = self.acc_manager.check_logged_in_credentials(user_name=data['username'], user_id=data['userID'])
            if not check:
                self.__set_response(400)
