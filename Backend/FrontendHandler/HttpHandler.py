import json
from http.server import BaseHTTPRequestHandler

import mysql

from BackendServices.AccountManager import AccountManager
from BackendServices.DungeonManager import DungeonManager
from DatabaseHandler.DatabaseHandler import *
from DatabaseHandler.User import *
from DungeonPackage.ActiveDungeon import *


class HTTPHandler(BaseHTTPRequestHandler):

    acc_manager = AccountManager()
    dung_manager = DungeonManager()

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
        print(post_data_raw)
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
            print("rooms as json returned: " + str(rooms))
            self.wfile.write(rooms)

        if self.path == '/getRaces':
            self.__set_response()
            dungeon_manager = DungeonManager()
            races = dungeon_manager.get_all_from_races_as_json(data)
            self.wfile.write(races)

        if self.path == '/getClasses':
            self.__set_response()
            dungeon_manager = DungeonManager()
            classes = dungeon_manager.get_all_from_classes_as_json(data)
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

        if self.path == '/saveDungeon':
            self.__set_response()
            dungeon_manager = DungeonManager(data)
            print("successfully created DungeonManager!")
            dungeon_id = dungeon_manager.write_dungeon_to_database()
            print("successfully executed Database transaction! Dungeon ID: " + dungeon_id)
            try:
                self.wfile.write(json.dumps(dungeon_id).encode(encoding='utf_8'))
            except IOError:
                pass
            # noch items und so abspeichern

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
