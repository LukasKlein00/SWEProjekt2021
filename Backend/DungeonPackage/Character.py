from DatabaseHandler.DatabaseHandler import DatabaseHandler
from DungeonPackage.Inventory import *


class Character:
    def __init__(self, life_points: int = 100, name: str = None, description: str = None, class_id: int = None, race_id: int = None,
                 user_id: str = None, room_id: str = None, inventory: Inventory = None, dungeon_id: str = None, discovered_rooms: [str] = [], character_id:str = None):
        self.life_points = life_points
        self.name = name
        self.description = description
        self.class_id = class_id
        self.race_id = race_id
        self.user_id = user_id
        self.room_id = room_id
        self.inventory = inventory
        self.dungeon_id = dungeon_id
        self.character_id = character_id
        self.discovered_rooms = discovered_rooms
        self.db_handler = DatabaseHandler()

    def load_data(self, user_id: str, dungeon_id: str):
        db_handler = DatabaseHandler()
        try:
            databaseCharacterData = db_handler.get_character_by_user_id(user_id, dungeon_id)
            self.life_points = databaseCharacterData["Lifepoints"]
            self.name = databaseCharacterData["CharacterName"]
            self.description = databaseCharacterData["CharacterDescription"]
            self.class_id = databaseCharacterData["ClassID"]
            self.race_id = databaseCharacterData["RaceID"]
            self.user_id = user_id
            #TODO: self.discovered_map = databaseCharacterData["RoomID"]
            self.dungeon_id = dungeon_id
            return self
        except:
            print("Ich bin eine exception")
            return None

    def add_item_to_inventory(self, item_id: str):
        self.db_handler.add_item_to_inventory(item_id, self.user_id, self.dungeon_id)

    def to_dict(self):
        return {'characterID': self.character_id, 'name': self.name, 'description': self.description,
                'health': self.life_points, 'classID': self.class_id, 'raceID': self.race_id,
                'userID': self.user_id, 'roomID': self.room_id, 'inventory': self.db_handler.get_inventory_by_dungeon_user_id(self.dungeon_id, self.user_id)}
