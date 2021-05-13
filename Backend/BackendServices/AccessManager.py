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

from DatabaseHandler.DatabaseHandler import *


class AccessManager:
    def __init__(self):
        self.db_handler = DatabaseHandler()

    def user_status_on_access_list(self, dungeon_id: str, user_name: str):
        ret = self.db_handler.user_status_on_access_list(user_name, dungeon_id)
        return bool(ret[0]) if ret else None
      #if ret:
      #    ret_zerro = bool(ret[0])
      #    return ret_zerro
      #else:
      #    return None

    def get_accesslist_for_dungeon(self):
        raise NotImplementedError

    def send_access_request_to_dm(self):
        raise NotImplementedError

    def join_user_to_white_list(self, user_id: str, dungeon_id: str):
        raise NotImplementedError

    def join_user_to_black_list(self, user_id: str, dungeon_id: str):
        raise NotImplementedError
