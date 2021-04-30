from BackendClasses.WebSocketHandler import *
import websockets
import asyncio
from http.server import HTTPServer
from BackendClasses.HTTPHandler import HTTPHandler
from threading import Thread

def startHTTP():
    print("Starting HTTPServer...\n")
    serverAddress = ('', 1188)
    http = HTTPServer(serverAddress, HTTPHandler)
    print('HTTPServer is running!')
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        pass
    http.server_close()


def startWS():
    loop = asyncio.new_event_loop()
    print('Starting WebsocketServer... \n')
    start_server = websockets.serve(WebSocketHandler, '', 1187, loop=loop)
    print('WebsocketServer is running!')
    loop.run_until_complete(start_server)
    loop.run_forever()


if __name__ == '__main__':
    Thread(target=startHTTP).start()
    Thread(target=startWS).start()
