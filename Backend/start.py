import eventlet

from FrontendHandler.WebsocketHandler import SocketIOHandler
import websockets
import asyncio
from http.server import HTTPServer
from FrontendHandler.HttpHandler import HTTPHandler
from threading import Thread

def start_HTTP():
    print("Starting HTTPServer...\n")
    serverAddress = ('', 1188)
    http = HTTPServer(serverAddress, HTTPHandler)
    print('HTTPServer is running!')
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        pass
    http.server_close()


def start_WS():
    """ws = WebSocketHandler
    loop = asyncio.new_event_loop()
    print('Starting WebsocketServer... \n')
    start_server = websockets.serve(ws.handle, '', 1187, loop=loop)
    print('WebsocketServer is running!')
    loop.run_until_complete(start_server)
    loop.run_forever()"""
    socketio = SocketIOHandler()
    eventlet.wsgi.server(eventlet.listen(('localhost', 5000)), socketio.app)


if __name__ == '__main__':
    Thread(target=start_HTTP).start()
    Thread(target=start_WS).start()
