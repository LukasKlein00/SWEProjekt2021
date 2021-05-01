import json
from http.server import BaseHTTPRequestHandler

import mysql

from BackendServices.AccountManager import AccountManager
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
        try:
            data = json.loads(post_data_raw)  # <--Daten als JSON-Objekt
            print(data)
        except:
            data = None

        if self.path == '/register':
            self._set_response()

            self.AccManager.registerUser(UserID=data['userID'], Firstname=data['firstName'], Lastname=data['lastName'],
                                    Username=data['username'], Email=data['email'], Password=data['password'],
                                    IsConfirmed=False)

            # Antwort senden? self.wfile.write(json.dumps("moin").encode(encoding='utf_8'))

        if self.path == '/login':
            self._set_response()
            response = self.AccManager.checkLoginCredeantials(Username=data['username'], Password=data['password'])
            if response:
                self.wfile.write(json.dumps(response).encode(encoding='utf_8'))
            else:
                self._set_response(400)

        if self.path == '/getMyDungeons':
            self._set_response()
            response = self.mDBHandler.getDungeonByID(data)
            self.wfile.write(json.dumps(response).encode(encoding='utf_8'))

        if self.path == '/saveDungeon':
            self._set_response()
            newDungeon = DungeonData(dungeonDescription=data['dungeonDescription'], dungeonName=data['dungeonName'],
                                     dungeonID=data['dungeonID'], maxPlayers=data['maxPlayers'],
                                     private=data['private'],
                                     dungeonMasterID=data['dungeonMasterID'])
            dungeonID = self.mDBHandler.saveOrUpdateDungeon(newDungeon)
            # noch items und so abspeichern

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
