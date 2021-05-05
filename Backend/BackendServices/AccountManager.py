import mysql
import json
from DatabaseHandler.User import User
from DatabaseHandler.DatabaseHandler import DatabaseHandler

from EmailServices.EmailSender import EmailSender
from EmailServices.messageType import messageType


class AccountManager:
    '''
    Class for handling Account Data
    '''

    def __init__(self):
        '''
        Constructor for AccountManager
        '''
        self.mDBHandler = DatabaseHandler()

    def register_user(self, user_id: str, firstname: str, lastname: str, username: str, email: str, password: str,
                      is_confirmed: bool) -> bool:
        '''
        initiate new User and hand over to DatabaseHandler.
        :param user_id: id of user
        :param firstname: firstname of user
        :param lastname: lastname of user
        :param username: username
        :param email: users email
        :param password: user password
        :param is_confirmed: is the account already confirmed?
        :return: if DatabaseHandler transaction worked, return true
        '''
        new_user = User(user_id, firstname, lastname, username, email, password, is_confirmed)
        # sendRegistrationEmail()
        check_method = self.mDBHandler.register_user(new_user)
        print(check_method)
        if check_method:
            return True
        else:
            return False

    def send_registration_email(self, email: str, user_id: str):
        '''
        sends registration email
        :param user_id: id of user
        '''
        print(email)
        email_sender = EmailSender(user_email=email, user_id=user_id)
        email_sender.send_email(messageType.registration)

    def check_login_credentials(self, username: str, password: str):
        '''
        initiate user with input parameters and hand it over to DatabaseHandler method "login_user", if it worked return username and id
        :param username: name of user
        :param password: password of user
        :return: username and id of corresponding user
        '''
        check_user = User(userName=username, password=password)
        returned_user_data = self.mDBHandler.login_user(check_user)
        returned_user = User(userID=returned_user_data[1], userName=returned_user_data[0],
                            confirmation=bool(returned_user_data[2]))
        if returned_user:
            response = {
                'username': returned_user.username,
                'user_id': returned_user.userID,
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
        :param user_id: id of user
        '''
        user_id = self.mDBHandler.get_user_id_by_email(user_email)
        password_vergessen_email = EmailSender(user_email, user_id)
        password_vergessen_email.send_email(messageType.reset_password)

    def change_password_in_database(self, user_id: str, password: str):
        '''
        hand over user_id and password to DatabaseHandler method "update_password_by_user_id"
        :param user_id: id of user
        :param password: password if user
        :return: true if transaction was successful
        '''
        updated_password = self.mDBHandler.update_password_by_user_id(user_id, password)
        return updated_password

    def delete_user(self, user_id: str):
        '''
        hand over userid to DatabaseHandler method "deleteUserById"
        :param user_id: id of user
        :return: True
        '''
        deleted_user = self.mDBHandler.delete_user_by_id(user_id)
        return deleted_user

    def confirm_registration_token(self, user_id: str):
        '''
        takes user_id and change the isConfirmed field in Database from False to True
        :param user_id: id of user
        '''
        self.mDBHandler.change_registration_status(userID=user_id)

    def check_logged_in_credentials(self, user_id: str, user_name: str):
        '''
        checks if user is already in database, when client is already logged in
        :param user_id: id of user
        :param user_name: username
        :return: return true if successful
        '''
        check_user = User(userName=user_name, userID=user_id)
        check = self.mDBHandler.check_user(user=check_user)
        return check
