class Room:
    def __init__(self, coordinate_x: int = None, coordinate_y: int = None, room_id: str= None, dungeon_id: str = None,
                 room_description: str = None, room_name: str = None,
                 is_start_room: bool = False, north: bool = True, south: bool = True, west: bool = True,
                 east: bool = True,
                 user_ids: [str] = [], npc_id: str = None, item_id: str = None):

        self.user_ids = user_ids
        self.coordinate_x = coordinate_x
        self.coordinate_y = coordinate_y
        self.room_id = room_id
        self.dungeon_id = dungeon_id
        self.npc_id = npc_id
        self.item_id = item_id
        self.room_description = room_description
        self.room_name = room_name
        self.is_start_room = is_start_room
        self.north = north
        self.south = south
        self.west = west
        self.east = east
