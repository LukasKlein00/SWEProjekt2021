#!/usr/bin/env python
__author__ = "Lukas Klein & Thomas Zimmermann"
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
__maintainer__ = "Lukas Klein & Thomas Zimmermann"
__email__ = "mudcake@gmail.com"
__status__ = "Development"

import mysql
import json
from DatabaseHandler.User import User
from DatabaseHandler.DatabaseHandler import DatabaseHandler

from EmailServices.EmailSender import EmailSender
from EmailServices.MessageType import MessageType


class AccountManager:
    '''
    Class for handling Account Data
    '''

    def __init__(self):
        '''
        Constructor for AccountManager
        '''
        self.db_handler = DatabaseHandler()

    def register_user(self, user_id: str, first_name: str, last_name: str, user_name: str, e_mail: str, password: str,
                      is_confirmed: bool) -> bool:
        '''
        initiate new User and hand over to DatabaseHandler.
        :param user_id: id of user
        :param first_name: firstname of user
        :param last_name: lastname of user
        :param user_name: username
        :param e_mail: users email
        :param password: user password
        :param is_confirmed: is the account already confirmed?
        :return: if DatabaseHandler transaction worked, return true
        '''
        new_user = User(user_id, first_name, last_name, user_name, e_mail, password, is_confirmed)
        # sendRegistrationEmail()
        check_method = self.db_handler.register_user(new_user)
        print(check_method)
        if check_method:
            return True
        else:
            return False

    def send_registration_email(self, email: str, userID: str):
        '''
        sends registration email
        :param UserID: id of user
        '''
        print(email)
        email_sender = EmailSender(user_email=email, user_id=userID)
        email_sender.send_email(MessageType.registration)

    def check_login_credentials(self, Username: str, Password: str):
        '''
        initiate user with input parameters and hand it over to DatabaseHandler method "login_user", if it worked return username and id
        :param Username: name of user
        :param Password: password of user
        :return: username and id of corresponding user
        '''
        checkUser = User(user_name=Username, password=Password)
        returned_user_data = self.db_handler.login_user(checkUser)
        returned_user = User(user_id=returned_user_data[1], user_name=returned_user_data[0],
                            confirmation=bool(returned_user_data[2]))
        if returned_user:
            response = {
                'username': returned_user.user_name,
                'userID': returned_user.user_id,
                'confirmation': returned_user.confirmation
            }

            if returned_user.confirmation:
                return response
            else:
                raise ValueError
            # self.wfile.write(json.dumps(response).encode(encoding='utf_8'))
        # else:
        # self.__set_response(400)

    def send_password_reset_email(self, user_email: str):
        '''
        Gets UserId from DatabaseHandler and gives it to Emailsender
        :param UserID: id of user
        '''
        user_id = self.db_handler.get_user_id_by_email(user_email)
        reset_password_email = EmailSender(user_email, user_id)
        reset_password_email.send_email(MessageType.reset_password)

    def change_password_in_database(self, user_id: str, password: str):
        '''
        hand over UserID and Password to DatabaseHandler method "update_password_by_user_id"
        :param user_id: id of user
        :param password: password if user
        :return: true if transaction was successful
        '''
        updated_password = self.db_handler.update_password_by_user_id(user_id, password)
        return updated_password

    def delete_user(self, user_id: str):
        '''
        hand over userid to DatabaseHandler method "deleteUserById"
        :param user_id: id of user
        :return: True
        '''
        deleted_user = self.db_handler.delete_user_by_id(user_id)
        return deleted_user

    def confirm_registration_token(self, user_id: str):
        '''
        takes userID and change the isConfirmed field in Database from False to True
        :param user_id: id of user
        '''
        self.db_handler.change_registration_status(user_id=user_id)

    def check_logged_in_credentials(self, user_id: str, user_name: str):
        '''
        checks if user is already in database, when client is already logged in
        :param user_id: id of user
        :param user_name: username
        :return: return true if successful
        '''
        check_user = User(user_name=user_name, user_id=user_id)
        check = self.db_handler.check_user(user=check_user)
        return check
