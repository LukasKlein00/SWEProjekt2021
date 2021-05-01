from DungeonPackage.ActiveDungeon import ActiveDungeon
from DungeonPackage.DungeonData import DungeonData
from DungeonPackage.Room import Room
from DungeonPackage.AccessList import AccessList
import uuid


class DungeonManager:
    def __init__(self):
        return

    def writeDungeonToDatabase(self, data):
        accessList = AccessList()
        roomList = data['rooms']
        raceList = data['races']
        classList = data['classes']
        itemList = data['items']
        npcList = data['npcs']

        for dataForUser in data['accessList']:
            accessList.addUserToAccessList(dataForUser['user'], dataForUser['isAllowed'])

        for room in data['rooms']:
            roomList.append(
                Room(coordinates=[room['x'], room['y']], roomID=(str(uuid.uuid4())), dungeonID=data['dungeonID'],
                     roomDescription=room['description'], roomName=room['name'], isStartRoom=room['isStartRoom'],
                     north=(bool(room['north'])), south=(bool(room['south'])), west=(bool(room['west'])),
                     east=bool((room['east']))))
        dungeonData = DungeonData(dungeonId=(str(uuid.uuid4())), dungeonMasterID=data['dungeonMasterID'],
                                  name=data['dungeonName'], description=data['dungeonDescription'],
                                  maxPlayers=data['maxPlayers'], private=data['private'], accessList=accessList)
        dungeon = ActiveDungeon(None, None, None, None, None, None, None, dungeonData=dungeonData)
        raise NotImplementedError

    def loadDungeonFromDatabase(self):
        ######
        raise NotImplementedError

    def deleteDungeonFromDatabase(self):
        #######
        raise NotImplementedError

    def copyDungeon(self):
        #####
        raise NotImplementedError

    def makeDungeonPrivate(self):
        raise NotImplementedError

    def makeDungeonPublic(self):
        raise NotImplementedError
