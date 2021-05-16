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

from DatabaseHandler.DatabaseHandler import DatabaseHandler
from DungeonPackage.Item import Item


class Inventory:
    def __init__(self, dungeon_id: str = None, user_id: str = None, inventory_id: str= None, items: [Item] = []):
        self.inventory_id = inventory_id
        self.dungeon_id = dungeon_id
        self.user_id = user_id
        self.items = items
        self.db_handler = DatabaseHandler()

    def delete_inventory(self):
        self.db_handler.remove_inventory_by_userid_dungeonid(self.dungeon_id, self.user_id)

    def add_item_to_inventory(self, item_id: str, item: Item = None):
        if item:
            self.items.append(item)
            self.db_handler.add_item_to_inventory(item.item_id, self.user_id, self.dungeon_id)
        else:
            self.db_handler.add_item_to_inventory(item_id, self.user_id, self.dungeon_id)

    def remove_item_from_inventory(self, item_id: str):
        self.db_handler.remove_item_from_inventory(item_id, self.user_id, self.dungeon_id)

    def get_inventory(self):
        all_items = self.db_handler.get_inventory_by_dungeon_user_id(self.dungeon_id, self.user_id)
        for item in all_items:
            if self.items.__len__() == 0:
                self.items.append(
                    Item(item_id=item['itemID'], description=item['itemDescription'], name=item['itemName']))
            for existing_item in self.items:
                if not item['itemID'] in existing_item.item_id:
                    self.items.append(
                        Item(item_id=item['itemID'], description=item['itemDescription'], name=item['itemName']))
        return self

    def to_dict(self):
        items_dict = []
        for item in self.items:
            items_dict.append(item.to_dict())
        return {'dugneonID': self.dungeon_id, 'user_id': self.user_id, 'items': items_dict}
