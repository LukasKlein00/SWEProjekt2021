from BackendClasses.WebSocketHandler import *
import websockets
import asyncio
from http.server import HTTPServer
from BackendClasses.HTTPHandler import HTTPHandler
from multiprocessing import Process

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
    print('Starting WebsocketServer... \n')
    start_server = websockets.serve(WebSocketHandler, '', 1187)
    print('WebsocketServer is running!')
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


if __name__ == '__main__':
    Process(target=startHTTP).start()
    Process(target=startWS).start()
