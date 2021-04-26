from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from BackendClasses.User import User
from BackendClasses.Dungeon import Dungeon
from BackendClasses.DatabaseHandler import DatabaseHandler
import mysql.connector

# Server
class S(BaseHTTPRequestHandler):
    mDBHandler = DatabaseHandler(mysql.connector.connect(
        host="193.196.53.67",
        port="1189",
        user="jack",
        password="123123"
    ))

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
        except:
            data = None

        if self.path == '/register':
            self._set_response()
            newUser = User(userID=data['userID'], firstName=data['firstName'], lastName=data['lastName'],
                           eMail=data['email'], userName=data['username'], password=data['password'],
                           confirmation=False)
            self.mDBHandler.registerUser(newUser)

            # Antwort senden? self.wfile.write(json.dumps("moin").encode(encoding='utf_8'))

        if self.path == '/login':
            self._set_response()
            newUser = User(userName=data['username'], password=data['password'])
            returnedUser = self.mDBHandler.loginUser(newUser)
            if returnedUser:
                response = {
                    'username': returnedUser.userName,
                    'userID': returnedUser.userID
                }
                self.wfile.write(json.dumps(response).encode(encoding='utf_8'))
            else:
                self._set_response(400)

        if self.path == '/getMyDungeons':
            self._set_response()
            response = self.mDBHandler.getDungeonByID(data)
            self.wfile.write(json.dumps(response).encode(encoding='utf_8'))

        if self.path == '/saveDungeon':
            self._set_response()
            newDungeon = Dungeon(dungeonDescription=data['dungeonDescription'], dungeonName=data['dungeonName'],
                                 dungeonID=data['dungeonID'], maxPlayers=data['maxPlayers'], private=data['private'],
                                 dungeonMasterID=data['dungeonMasterID'])
            dungeonID = self.mDBHandler.saveOrUpdateDungeon(newDungeon)
            #noch items und so abspeichern

        if self.path == '/deleteDungeon':
            self._set_response()
            self.mDBHandler.deleteDungeonByID(data)

        if self.path == '/deleteUser':
            self._set_response()
            self.mDBHandler.deleteUserByID(data)

        if self.path == '/copyDungeon':
            print(data)
            self._set_response()
            #self.mDBHandler.copyDungeon(data)



# Startet den Server
def run(server_class=HTTPServer, handler_class=S):
    print("Starting HTTP Server...")
    server_address = ('', 1188)
    http = server_class(server_address, handler_class)
    print("Started!")
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        pass
    http.server_close()


# Main-Methode wird beim Starten der Datei ausgeführt
if __name__ == '__main__':
    run()
