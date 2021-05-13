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

class User:
    """
    User Class
    """
    def __init__(self, user_id: str = None, first_name: str = None, last_name: str = None, user_name: str = None,
                 e_mail: str = None, password: str = None, confirmation: bool = False):
        """
        constructor of user class
        """         
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.user_name = user_name
        self.e_mail = e_mail
        self.password = password
        self.confirmation = confirmation
