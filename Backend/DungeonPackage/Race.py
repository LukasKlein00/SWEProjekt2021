from DatabaseHandler.DatabaseHandler import *


class Race:

    def __init__(self, race_id: str = None, name: str = None, description: str= None, dungeon_id: str= None):
        self.race_id = race_id
        self.name = name
        self.description = description
        self.dungeon_id = dungeon_id

    def load_data(self, dungeon_id: str):
        db_handler = DatabaseHandler()
        database_race = db_handler.get_race_by_dungeon_id(dungeon_id)
        self.race_id = database_race[0]
        self.name = database_race[1]
        self.description = database_race[2]
        self.dungeon_id = dungeon_id
