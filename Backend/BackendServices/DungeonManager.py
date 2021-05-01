from DungeonPackage.ActiveDungeon import ActiveDungeon
from DungeonPackage.Class import Class
from DungeonPackage.DungeonData import DungeonData
from DungeonPackage.Item import Item
from DungeonPackage.Npc import Npc
from DungeonPackage.Race import Race
from DungeonPackage.Room import Room
from DungeonPackage.AccessList import AccessList
import uuid


class DungeonManager:
    def __init__(self):
        return

    def writeDungeonToDatabase(self, data):
        accessList = AccessList()
        room_data = data['rooms']
        race_data = data['races']
        class_data = data['classes']
        items_data = data['items']
        npcs_data = data['npcs']

        room_list = list(Room)
        race_list = list(Race)
        class_list = list(Class)
        items_list = list(Item)
        npcs_list = list(Npc)




        for dataForUser in data['accessList']:
            accessList.addUserToAccessList(dataForUser['user'], dataForUser['isAllowed'])

        for room in data['rooms']:
            room_list.append(
                Room(coordinate_x=[room['x']], coordinate_y=[room['y']], room_id=(str(uuid.uuid4())), dungeon_id=data['dungeonID'],
                     room_description=room['description'], room_name=room['name'], is_start_room=room['isStartRoom'],
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
