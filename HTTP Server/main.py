from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import post

login = {
    'username': 'Testuser',
    'password': 'testpassword'    
}
dummyData = json.dumps(login)


#Server
class S(BaseHTTPRequestHandler):
    #übermittelt Einstellungen "Headers" des Requests
    def _set_response(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Methods', 'POST')
        self.send_header('Access-Control-Allow-Headers', 'Authorization, Content-Type')
        self.end_headers()


    #OPTIONS Request: Wird vor jeder Request ausgeführt, um zu checken, ob die Request erlaubt ist
    def do_OPTIONS(self):
        print("Request received!")
        self._set_response()      


    #GET Request: "Wird verwendet wenn Daten ausgegeben werden ohne Dateninput"
    def do_GET(self):
        #wenn an *ip*/showMaps gesendet wird...
        if (self.path == '/showMaps'):
            self._set_response()

            #   "code der alle Namen und Spielerzahlen aller erstellten MUDS durchsucht"

            #Beispielobjekt für Antwort
            replyMaps = [{
                'mapName': 'myNewMUD',
                'mapID': 1,
                'maxPlayers': 10,
                'currentPlayers': 3,
            },
            {
                'mapName': 'myNewMUD2',
                'mapID': 1,
                'maxPlayers': 10,
                'currentPlayers': 4,
            }]

            #sendet Antwort
            self.wfile.write(json.dumps(replyMaps).encode(encoding='utf_8'))
        

    #GET Request: "Wird verwendet wenn Daten ausgegeben werden mit Dateninput"
    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Größe der Daten
        post_data_raw = self.rfile.read(content_length) # <--- Erfasst die Daten
        data = json.loads(post_data_raw) # <--Daten als JSON-Objekt

        #wenn an *ip*/Login gesendet wird...
        if (self.path == '/login'):
            username = dummyData['username']
            password = dummyData['password']
            # "code für Datenbank abfrage"
            
            replyLoginData = {
                'token': '371bd71e21be81e1v',
                'username': 'HeinzGünther',
                'userid': 2
            }

            self._set_response()
            self.wfile.write(json.dumps(replyLoginData).encode(encoding='utf_8'))


        ##Weitermachen
        if (self.path == '/saveDungeon'):
            print("safe Dungeon")
            try:
                response = post.saveOrUpdateDungeon(data)
                print(response)
                self._set_response()
                self.wfile.write(json.dumps(response).encode(encoding='utf_8'))
            except IOError:
                print("failed")


#Startet den Server
def run(server_class=HTTPServer, handler_class=S):
    print("Starting Server...")
    server_address = ('', 1188)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        pass
    http.server_close()


#Main-Methode wird beim Starten der Datei ausgeführt
if __name__ == '__main__':
    run()