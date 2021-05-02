from DatabaseHandler.DatabaseHandler import *


class Class:
    def __init__(self, class_id: str, name: str, description: str, dungeon_id: str):
        self.classID = class_id
        self.name = name
        self.description = description
        self.dungeon_id = dungeon_id
        self.mDBHandler = DatabaseHandler()

    def loadData(self, dungeonID: str):
        databaseClassData = self.mDBHandler.get_class_by_dungeon_ID(dungeonID)
        self.classID = databaseClassData[0]
        self.name = databaseClassData[1]
        self.description = databaseClassData[2]
        self.dungeon_id = databaseClassData[3]
