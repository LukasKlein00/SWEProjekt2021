from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import post
import get

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
        self.send_header('Access-Control-Allow-Methods', 'POST, GET')
        self.send_header('Access-Control-Allow-Headers', 'Authorization, Content-Type')
        self.end_headers()


    #OPTIONS Request: Wird vor jeder Request ausgeführt, um zu checken, ob die Request erlaubt ist
    def do_OPTIONS(self):
        print("Request received!")
        self._set_response()      


    #GET Request: "Wird verwendet wenn Daten ausgegeben werden sollen"
    def do_GET(self):
        pass
        
        

    #POST Request: "Wird verwendet wenn Daten angenommen werden sollen"
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


        ##Dungeon speichern oder updaten
        if (self.path == '/saveDungeon'):
            print("safe Dungeon")
            try:
                response = post.saveOrUpdateDungeon(data)
                print(response)
                self._set_response()
                self.wfile.write(json.dumps(response).encode(encoding='utf_8'))
            except:
                pass

        if (self.path == '/users/register'):
            print("register User")
            response = post.regiserUser(data)
            print(response)
            self._set_response()
            self.wfile.write(json.dumps(response).encode(encoding='utf_8'))

        if (self.path == '/users/login'):
                    print("login User")
                    response = post.loginUser(data)
                    if response:
                        print(response)
                        self._set_response()
                        self.wfile.write(json.dumps(response).encode(encoding='utf_8'))

        if (self.path == '/getMyDungeons'):
                    print("getMyDungeons")
                    response = post.getMyDungeons(data)
                    if response:
                        print(response)
                        self._set_response()
                        self.wfile.write(json.dumps(response).encode(encoding='utf_8'))
        
        if (self.path == '/getDungeon'):
                    print("getDungeon")
                    response = post.getDungeon(data)
                    if response:
                        print(response)
                        self._set_response()
                        self.wfile.write(json.dumps(response).encode(encoding='utf_8'))
                


#Startet den Server
def run(server_class=HTTPServer, handler_class=S):
    print("Starting Server...")
    server_address = ('', 1188)
    http = server_class(server_address, handler_class)
    print("Started!")
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        pass
    http.server_close()


#Main-Methode wird beim Starten der Datei ausgeführt
if __name__ == '__main__':
    run()