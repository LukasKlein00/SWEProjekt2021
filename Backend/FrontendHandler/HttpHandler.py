import json
from http.server import BaseHTTPRequestHandler

import mysql

from BackendServices.AccountManager import AccountManager
from BackendServices.DungeonManager import DungeonManager
from DatabaseHandler.DatabaseHandler import *
from DatabaseHandler.User import *
from DungeonPackage.ActiveDungeon import *


class HTTPHandler(BaseHTTPRequestHandler):


    AccManager = AccountManager()

    # übermittelt Einstellungen "Headers" des Requests
    def _set_response(self, code: int = 200):
        self.send_response(code)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET')
        self.send_header('Access-Control-Allow-Headers', 'Authorization, Content-Type')
        self.end_headers()

    # OPTIONS Request: Wird vor jeder Request ausgeführt, um zu checken, ob die Request erlaubt ist
    def do_OPTIONS(self):
        self._set_response()

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
            print(data)
        except:
            data = None

        if self.path == '/confirm':
            self._set_response()
            try:
                self.AccManager.confirm_registration_token(data['token'])
            except:
                print("/confirm received but error")
                pass

        if self.path == '/register':
            self._set_response()
            print(self.path)
            try:
                self.AccManager.registerUser(UserID=data['userID'], Firstname=data['firstName'], Lastname=data['lastName'],
                                    Username=data['username'], Email=data['email'], Password=data['password'],
                                    IsConfirmed=False)

                self.AccManager.send_registration_email(data['email'], data['userID'])
            except:
                pass

            # Antwort senden? self.wfile.write(json.dumps("moin").encode(encoding='utf_8'))

        if self.path == '/login':
            self._set_response()
            try:
                response = self.AccManager.checkLoginCredentials(Username=data['username'], Password=data['password'])
                self.wfile.write(json.dumps(response).encode(encoding='utf_8'))
            except:
                self._set_response(400)

        if self.path == '/getMyDungeons':
            self._set_response()
            response = self.mDBHandler.getDungeonByID(data)
            self.wfile.write(json.dumps(response).encode(encoding='utf_8'))

        if self.path == '/saveDungeon':
            self._set_response()
            """newDungeon = DungeonData(dungeonDescription=data['dungeonDescription'], dungeonName=data['dungeonName'],
                                     dungeonID=data['dungeonID'], maxPlayers=data['maxPlayers'],
                                     private=data['private'],
                                     dungeonMasterID=data['dungeonMasterID'])"""
            dungeon_manager = DungeonManager(data)
            dungeon_id = dungeon_manager.write_dungeon_to_database()
            self.wfile.write(json.dumps(dungeon_id).encode(encoding='utf_8'))

        if self.path == '/deleteDungeon':
            self._set_response()
            self.mDBHandler.deleteDungeonByID(data)

        if self.path == '/deleteUser':
            self._set_response()
            deletetransaction = self.AccManager.deleteUser(UserID=data)
            if not deletetransaction:
                self._set_response(400)

        if self.path == '/copyDungeon':
            print(data)
            self._set_response()
            # self.mDBHandler.copyDungeon(data)

        if self.path == '/forgotPassword':
            self._set_response()
            self.AccManager.sendPasswordResetEmail(UserID=data['userID'], UserEmail=data['email'])

        if self.path == '/resetPassword':
            self._set_response()
            isPasswordChanged = self.AccManager.changePasswordInDatabase(UserID=data['userID'], Password=data['password'])
            if not isPasswordChanged:
                self._set_response(400)