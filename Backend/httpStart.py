from http.server import HTTPServer
from BackendClasses.HTTPHandler import HTTPHandler

# Main-Methode wird beim Starten der Datei ausgeführt
if __name__ == '__main__':
    print("Starting HTTP Server...")
    serverAddress = ('', 1188)
    http = HTTPServer(serverAddress, HTTPHandler)
    print("Started!")
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        pass
    http.server_close()
