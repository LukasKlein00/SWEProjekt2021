from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
import databasemodul

login = {
    'username': 'Testuser',
    'password': 'testpassword'    
}
dummyData = json.dumps(login)

class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Methods', 'POST')
        self.send_header('Access-Control-Allow-Headers', 'Authorization, Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_response()      



    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        if (self.path == '/users/authenticate'):           
            self._set_response()
            self.wfile.write(json.dumps(user).encode(encoding='utf_8'))
        

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself

        if (self.path == '/login'):
            pass



        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        if (self.path == '/users/authenticate'):
            d = json.loads(post_data)
            token = databasemodul.checkLogin(d['username'],d['password'])
            if token!=0:
                reply = {
                'username': d['username'],
                'token':  token
                }
                self._set_response()
                self.wfile.write(json.dumps(reply).encode(encoding='utf_8'))

        if (self.path == '/users/register'):
                    d = json.loads(post_data)
                    print(d)
                    added = databasemodul.addUser(d['username'],d['firstName'],d['lastName'],d['password'])
                    if added:
                        reply = {
                        'message': 'user added',
                        }
                        self._set_response()
                        self.wfile.write(json.dumps(reply).encode(encoding='utf_8'))
        


def run(server_class=HTTPServer, handler_class=S):
    logging.basicConfig(filename='./Info.log', filemode='w', level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    server_address = ('', 1188)
    http = server_class(server_address, handler_class)
    logging.info('Starting HTTP Server...\n')
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        pass
    http.server_close()
    logging.info('Stopping HTTP Server...\n')

if __name__ == '__main__':
    run()