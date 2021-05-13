#!/usr/bin/env python
__author__ = "Lukas Klein"
__copyright__ = "Copyright 2021, The MUDCake Project"
__credits__ = "Hauke Presig, Jack Drillisch, Jan Gruchott, Lukas Klein, Robert Fendrich, Thomas Zimmermann"

__license__ = """MIT License

                     Copyright (c) 2021 MUDCake Project

                     Permission is hereby granted, free of charge, to any person obtaining a copy
                     of this software and associated documentation files (the "Software"), to deal
                     in the Software without restriction, including without limitation the rights
                     to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
                     copies of the Software, and to permit persons to whom the Software is
                     furnished to do so, subject to the following conditions:

                     The above copyright notice and this permission notice shall be included in all
                     copies or substantial portions of the Software.

                     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
                     IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
                     FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
                     AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
                     LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
                     OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
                     SOFTWARE."""

__version__ = "1.0.0"
__maintainer__ = "Lukas Klein"
__email__ = "mudcake@gmail.com"
__status__ = "Development"

from DungeonPackage.ActiveDungeon import ActiveDungeon
from DungeonPackage.DungeonData import DungeonData
from DungeonPackage.AccessList import AccessList

class ActiveDungeonHandler:
    def __init__(self):
        self.active_dungeon_ids = []
        self.sid_of_dungeon_master = dict()                         #sid_of_dungeon_master['dungeonID'] -> sidOfDungeonMaster
        self.active_dungeons = dict()                               #active_dungeons['dungeonID'] -> activeDungeon
        self.user_sid = dict()                                      #user_sid['user_id'] -> [user_sid]
        self.user_count_in_dungeon = dict()                         #user_count_in_dungeon['dungeonID'] -> numberOfUsers

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
