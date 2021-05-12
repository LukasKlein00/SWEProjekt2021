from DungeonPackage.ActiveDungeon import ActiveDungeon
from DungeonPackage.DungeonData import DungeonData
from DungeonPackage.AccessList import AccessList

class ActiveDungeonHandler:
    def __init__(self):
        self.active_dungeon_ids = []
        self.sid_of_dungeon_master = dict()                         #sid_of_dungeon_master['dungeonID'] -> sidOfDungeonMaster
        self.active_dungeons = dict()                               #active_dungeons['dungeonID'] -> activeDungeon
        self.user_sid = dict()                                      #user_sid['user_id'] -> user_sid

    def __init_dungeon(self, dungeon_id: str):
        return dict({'dungeon_data_object': DungeonData().load_data(dungeon_id),
                     'access_list_object': AccessList(dungeon_id=dungeon_id).load_data(),
                     'races_objects': dict(),                       #race_object['race_ID'] -> race_object
                     'classes_objects': dict(),                     #classes_object['class_ID'] -> class_object
                     'items_objects': dict(),                       #items_object['item_ID'] -> item_object
                     'characters_objects': dict(),                  #characters_object['character_ID'] -> character_object
                     'npcs_objects': dict(),                        #npcs_objects['npc_ID'] -> npc_object
                     'active_dungeon_object': ActiveDungeon()})

    def dungeon_join(self, dungeon_id):
        if not self.active_dungeon_ids.__contains__(dungeon_id):
            self.active_dungeon_ids.append(dungeon_id)
            self.active_dungeons[dungeon_id] = self.__init_dungeon(dungeon_id)

    def dungeon_leave(self, dungeon_id):
        self.active_dungeon_ids.remove(dungeon_id)
        del self.active_dungeons[dungeon_id]
