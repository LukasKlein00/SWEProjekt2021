#!/usr/bin/env python
__author__ = "Jan Gruchott"
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
__maintainer__ = "Jan Gruchott"
__email__ = "mudcake@gmail.com"
__status__ = "Development"

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
