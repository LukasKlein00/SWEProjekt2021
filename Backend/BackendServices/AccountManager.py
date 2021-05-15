# region HEADER
# !/usr/bin/env python
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
# endregion
from DatabaseHandler.User import User
from DatabaseHandler.DatabaseHandler import DatabaseHandler

from EmailServices.EmailSender import EmailSender
from EmailServices.MessageType import MessageType


class AccountManager:
    """" The main class for handling account based data

    It contains a database handler for managing access to the database.
    """

    def __init__(self):
        self.db_handler = DatabaseHandler()

    def register_user(self, user_id: str, first_name: str, last_name: str, user_name: str, e_mail: str, password: str,
                      is_confirmed: bool) -> bool:
        """ Adds user to database.

        Creates an instance of an user object.
        Then registers the user via the database.
        Lastly checks if the user has been written to the database successfully.

        Args:
            user_id (str): User id of the user to written to the database.
            first_name (str): Firstname of the registered user.
            last_name (str): Lastname of the registered user.
            user_name (str): Username of the registered user.
            e_mail (str): Email of the registered user .
            password (str): Password of the registered user.
            is_confirmed (bool): Initial confirmation status.

        Returns:
            True if the user has been successfully written to the database,
            False if an error occurred while registering.
        """

        new_user = User(user_id, first_name, last_name, user_name, e_mail, password, is_confirmed)
        check_method = self.db_handler.register_user(new_user)
        if check_method:
            return True
        else:
            return False

    @staticmethod
    def send_registration_email(email: str, userID: str):
        """ Sending registration email to the user

        First creates an object of the EmailSender with the needed parameters.
        Then calls send email to send the email via the EmailSender

        Args:
            email (str): Email of the user who is supposed to be receiving the email
            userID (str): User id of the user who is supposed to be receiving the email

        """
        email_sender = EmailSender(user_email=email, user_id=userID)
        email_sender.send_email(MessageType.registration)

    def check_login_credentials(self, Username: str, Password: str):
        """ Basic check of the login credentials in the database

        First creates an user object with the necessary data.
        After that it checks the user via the given database method.
        At the end the response gets created. Based on the confirmation status which has to
        be set to true via an email confirmation the method return an error or not.

        Args:
            Username (str): The username of the user which is supposed to be checked
            Password (str): The password of the user which is supposed to be checked

        Returns:
            An dictionary named response with the user data if the credentials were correct,
            Value Error if the email of the user hasn't been confirmed yet.
        """
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

    def send_password_reset_email(self, user_email: str):
        """ Sends the password reset email if the corresponding button is pressed

        Calls the database handler where the user id is fetched via the given email.
        Subsequently sends an password reset email via the EmailSender

        Args:
            user_email (str): The email of the user whose password is supposed to be reset

        """
        user_id = self.db_handler.get_user_id_by_email(user_email)
        reset_password_email = EmailSender(user_email, user_id)
        reset_password_email.send_email(MessageType.reset_password)

    def change_password_in_database(self, user_id: str, password: str):
        """ The action which gets called if the user clicked the link in the password reset email

        Simply calls the database handler and overwrites the password in it

        Args:
            user_id (str): User id of the user whose password is supposed to be reset
            password (str): The new password of the user

        Returns:
            True if the password has been reset correctly,
            False if an error occurred

        """
        updated_password = self.db_handler.update_password_by_user_id(user_id, password)
        return updated_password

    def delete_user(self, user_id: str):
        """ Basic method which gets called if the user presses the delete button

        Deletes the user via the corresponding database method

        Args:
            user_id (str): User id of the user who wants to delete his data

        Returns:
            True if the user has been deleted correctly,
            False if an error occurred

        """
        deleted_user = self.db_handler.delete_user_by_id(user_id)
        return deleted_user

    def confirm_registration_token(self, user_id: str):
        """ Gets called if the user clicks on the link send in the registration email

        The Token in the user email is the user id.
        Hence the database changes the confirmation to true at the given user id

        Args:
            user_id (str): User id of the user who clicked on the confirmation link

        """
        self.db_handler.change_registration_status(user_id=user_id)

    def check_logged_in_credentials(self, user_id: str, user_name: str):
        """ Checks if the user is already logged in

        Args:
            user_id (str): User if of the given user
            user_name (str): Username of the given user

        Returns:
            True if the user is already logged in,
            False if the user is not
        """
        check_user = User(user_name=user_name, user_id=user_id)
        check = self.db_handler.check_user(user=check_user)
        return check
