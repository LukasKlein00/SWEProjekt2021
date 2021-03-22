import asyncio
import websockets
import json

t = {
    'methode': 'chat',
    'content': {
        'content': 'hallo wie gehts',
        'userID': 2,
        'receiver': 'dungeonchat',
    }
}
dummyData = json.dumps(t)





connected = set()

async def server(websocket, path):
    connected.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)

            if data['methode'] == 'chat':
                pass

            if data['method'] == 'allchat':
                for conn in connected:
                    reply = {
                        'id': data['id'],
                        'msg': data['msg'],
                        'typ': 'chat'
                    }
                    await conn.send(json.dumps(reply))
            
            if data['method'] == 'action':
                reply = {
                        'id': data['id'],
                        'msg': data['msg'],
                        'typ': 'action'
                    }
                await websocket.send(json.dumps(reply))
    finally:
        connected.remove(websocket)
print('Starting WebsocketServer... \n')
start_server = websockets.serve(server, '', 1187)
print('Server is running!')

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()