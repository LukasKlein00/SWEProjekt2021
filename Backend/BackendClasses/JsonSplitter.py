j = '{"dungeonID":"b7ceabcc-feb9-4a4b-9856-50999364c7b2","dungeonMasterID":"85078788-b765-4f88-ab30-532a39611e22","dungeonName":"Newdungeon","dungeonDescription":"Newdungeon Description","maxPlayers":10,"rooms":[{"x":9,"y":3,"isActive":true},{"x":10,"y":3,"isActive":true},{"x":11,"y":3,"isActive":true},{"x":9,"y":4,"isActive":true},{"x":11,"y":4,"isActive":true},{"x":12,"y":4,"isActive":true},{"x":12,"y":5,"isActive":true},{"x":7,"y":6,"isActive":true},{"x":12,"y":6,"isActive":true},{"x":7,"y":7,"isActive":true},{"x":8,"y":7,"isActive":true},{"x":9,"y":7,"isActive":true},{"x":12,"y":7,"isActive":true},{"x":9,"y":8,"isActive":true},{"x":12,"y":8,"isActive":true},{"x":9,"y":9,"isActive":true},{"x":10,"y":9,"isActive":true},{"x":11,"y":9,"isActive":true},{"x":12,"y":9,"isActive":true}],"races":[{"name":"newRace","description":"newRaceDescription"}],"classes":[{"name":"newClass","description":"newClassDescription","equipment":null}],"items":[],"npcs":[],"private":false,"whiteList":[],"blackList":[]}'


import json


class JsonDeserializer(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)

p = JsonDeserializer(j)


print(p.dungeonID)
print(p.rooms[0])
print(p.items)


#Json umwandeln in Objekte
