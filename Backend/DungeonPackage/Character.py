from DatabaseHandler.DatabaseHandler import *
from DungeonPackage.Inventory import *


class Character:
    def __init__(self, character_id: str, life_points: int, name: str, description: str, class_id: int, race_id: int,
                 user_id: str, discovered_map_id: int, inventory: Inventory = None):
        self.character_id = character_id
        self.life_points = life_points
        self.name = name
        self.description = description
        self.class_id = class_id
        self.race_id = race_id
        self.user_id = user_id
        self.discovered_map = discovered_map_id
        self.inventory = inventory
        self.db_handler = DatabaseHandler()

    def load_data(self, dungeon_id: str):
        databaseCharacterData = self.db_handler.get_character_by_dungeon_ID(dungeon_id)
        self.character_id = databaseCharacterData[0]
        self.life_points = databaseCharacterData[1]
        self.name = databaseCharacterData[2]
        self.description = databaseCharacterData[3]
        self.class_id = databaseCharacterData[4]
        self.race_id = databaseCharacterData[5]
        self.user_id = databaseCharacterData[6]
        self.discovered_map = databaseCharacterData[7]
