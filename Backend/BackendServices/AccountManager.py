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

    def register_user(self, UserID: str, Firstname: str, Lastname: str, Username: str, Email: str, Password: str,
                      IsConfirmed: bool) -> bool:
        '''
        initiate new User and hand over to DatabaseHandler.
        :param UserID: id of user
        :param Firstname: firstname of user
        :param Lastname: lastname of user
        :param Username: username
        :param Email: users email
        :param Password: user password
        :param IsConfirmed: is the account already confirmed?
        :return: if DatabaseHandler transaction worked, return true
        '''
        newUser = User(UserID, Firstname, Lastname, Username, Email, Password, IsConfirmed)
        # sendRegistrationEmail()
        checkMethod = self.mDBHandler.register_user(newUser)
        print(checkMethod)
        if checkMethod:
            return True
        else:
            return False

    def send_registration_email(self, email: str, userID: str):
        '''
        sends registration email
        :param UserID: id of user
        '''
        print(email)
        email_sender = EmailSender(userEmail=email, userID=userID)
        email_sender.send_email(messageType.registration)

    def check_login_credentials(self, Username: str, Password: str):
        '''
        initiate user with input parameters and hand it over to DatabaseHandler method "login_user", if it worked return username and id
        :param Username: name of user
        :param Password: password of user
        :return: username and id of corresponding user
        '''
        checkUser = User(user_name=Username, password=Password)
        returnedUserData = self.mDBHandler.login_user(checkUser)
        returnedUser = User(user_id=returnedUserData[1], user_name=returnedUserData[0],
                            confirmation=bool(returnedUserData[2]))
        if returnedUser:
            response = {
                'username': returnedUser.userName,
                'userID': returnedUser.userID,
                'confirmation': returnedUser.confirmation
            }

            if returnedUser.confirmation:
                return response
            else:
                raise ValueError
            # self.wfile.write(json.dumps(response).encode(encoding='utf_8'))
        # else:
        # self.__set_response(400)

    def send_password_reset_email(self, UserEmail: str):
        '''
        Gets UserId from DatabaseHandler and gives it to Emailsender
        :param UserID: id of user
        '''
        userID = self.mDBHandler.get_user_id_by_email(UserEmail)
        passwordVergessenEmail = EmailSender(UserEmail, userID)
        passwordVergessenEmail.send_email(messageType.resetPassword)

    def change_password_in_database(self, UserID: str, Password: str):
        '''
        hand over UserID and Password to DatabaseHandler method "update_password_by_user_id"
        :param UserID: id of user
        :param Password: password if user
        :return: true if transaction was successful
        '''
        updatedPassword = self.mDBHandler.update_password_by_user_id(UserID, Password)
        return updatedPassword

    def delete_user(self, UserID: str):
        '''
        hand over userid to DatabaseHandler method "deleteUserById"
        :param UserID: id of user
        :return: True
        '''
        deletedUser = self.mDBHandler.delete_user_by_id(UserID)
        return deletedUser

    def confirm_registration_token(self, UserID: str):
        '''
        takes userID and change the isConfirmed field in Database from False to True
        :param UserID: id of user
        '''
        self.mDBHandler.change_registration_status(user_id=UserID)

    def check_logged_in_credentials(self, UserID: str, UserName: str):
        '''
        checks if user is already in database, when client is already logged in
        :param UserID: id of user
        :param UserName: username
        :return: return true if successful
        '''
        checkUser = User(user_name=UserName, user_id=UserID)
        check = self.mDBHandler.check_user(user=checkUser)
        return check
