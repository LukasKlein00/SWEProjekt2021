import logging
import socket

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
    ip = ""
    socketio = SocketIOHandler()
    host_name = socket.gethostname()
    if str(socket.gethostbyname(host_name)) != "193.196.53.67":
        ip = ip.replace("{Server}", "localhost:4200")
    else:
        ip = ip.replace("{Server}", "193.196.54.98")

    eventlet.wsgi.server(eventlet.listen((ip, 1187)), socketio.app, log_output=False)


if __name__ == '__main__':
    logging.getLogger('socketio').setLevel(logging.ERROR)
    logging.getLogger('engineio').setLevel(logging.ERROR)
    Thread(target=start_HTTP).start()
    Thread(target=start_WS).start()


