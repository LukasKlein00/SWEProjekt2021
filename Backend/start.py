#!/usr/bin/env python
__author__ = "Jack Drillisch"
__copyright__ = "Copyright 2021, The MUDCake Project"
__credits__ = "Hauke Presig, Jack Drillisch, Jan Gruchott, Lukas Klein, Robert Fendrich, Thomas Zimmermann"

__license__ = """MIT License

                     Copyright (c) 2021 MUDCake Project

                     Permission is hereby granted, free of charge, to any person obtaining a copy
                     of this software and associated documentation files (the "Software"), to deal
                     in the Software without restriction, including without limitation the rights
                     to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
                     copies of the Software, and to permit persons to whom the Software is
                     furnished to do so, subject to the following conditions:

                     The above copyright notice and this permission notice shall be included in all
                     copies or substantial portions of the Software.

                     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
                     IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
                     FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
                     AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
                     LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
                     OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
                     SOFTWARE."""

__version__ = "1.0.0"
__maintainer__ = "Jack Drillisch"
__email__ = "mudcake@gmail.com"
__status__ = "Development"

import logging
import socket

import eventlet

from FrontendHandler.WebsocketHandler import SocketIOHandler
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
    ip = ""
    socketio = SocketIOHandler()
    host_name = socket.gethostname()
    if str(socket.gethostbyname(host_name)) != "193.196.53.67":
        ip = ip.replace("{Server}", "localhost:4200")
    else:
        ip = ip.replace("{Server}", "193.196.54.98")

    eventlet.wsgi.server(eventlet.listen((ip, 1187)), socketio.app, log_output=False)


if __name__ == '__main__':
    logging.getLogger('mysql').setLevel(logging.ERROR)
    logging.getLogger('mysql-connector-python').setLevel(logging.ERROR)
    logging.getLogger('mysqlclient').setLevel(logging.ERROR)
    logging.getLogger('socketio').setLevel(logging.ERROR)
    logging.getLogger('engineio').setLevel(logging.ERROR)
    Thread(target=start_HTTP).start()
    Thread(target=start_WS).start()


