from BackendClasses.WebSocketHandler import *
import websockets
import asyncio

# Main-Methode wird beim Starten der Datei ausgeführt
if __name__ == '__main__':
    print('Starting WebsocketServer... \n')
    start_server = websockets.serve(WebSocketHandler, '', 1187)
    print('Server is running!')
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
