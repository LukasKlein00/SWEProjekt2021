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
        self.mDBHandler = DatabaseHandler(mysql.connector.connect(
            host="193.196.53.67",
            port="1189",
            user="jack",
            password="123123"
        ))

    def registerUser(self, UserID: str, Firstname: str, Lastname: str, Username: str, Email: str, Password: str,
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
        checkMethod = self.mDBHandler.registerUser(newUser)
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
        email_sender.sendEmail(messageType.registration)

    def checkLoginCredentials(self, Username: str, Password: str):
        '''
        initiate user with input parameters and hand it over to DatabaseHandler method "loginUser", if it worked return username and id
        :param Username: name of user
        :param Password: password of user
        :return: username and id of corresponding user
        '''
        checkUser = User(userName=Username, password=Password)
        returnedUser = self.mDBHandler.loginUser(checkUser)
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
        # self._set_response(400)

    def sendPasswordResetEmail(self, UserEmail: str):
        '''
        Gets UserId from DatabaseHandler and gives it to Emailsender
        :param UserID: id of user
        '''
        userID = self.mDBHandler.getUserIdByEmail(UserEmail)
        passwordVergessenEmail = EmailSender(UserEmail, userID)
        passwordVergessenEmail.sendEmail(messageType.resetPassword)

    def changePasswordInDatabase(self, UserID: str, Password: str):
        '''
        hand over UserID and Password to DatabaseHandler method "updatePasswordByUserID"
        :param UserID: id of user
        :param Password: password if user
        :return: true if transaction was successful
        '''
        updatedPassword = self.mDBHandler.updatePasswordByUserID(UserID, Password)
        return updatedPassword

    def deleteUser(self, UserID: str):
        '''
        hand over userid to DatabaseHandler method "deleteUserById"
        :param UserID: id of user
        :return: True
        '''
        deletedUser = self.mDBHandler.deleteUserByID(UserID)
        return deletedUser

    def confirm_registration_token(self, UserID: str):
        '''
        takes userID and change the isConfirmed field in Database from False to True
        :param UserID: id of user
        '''
        self.mDBHandler.change_registration_status(userID=UserID)

    def check_logged_in_credentials(self, UserID: str, UserName: str):
        '''
        checks if user is already in database, when client is already logged in
        :param UserID: id of user
        :param UserName: username
        :return: return true if successful
        '''
        checkUser = User(userName=UserName, userID=UserID)
        check = self.mDBHandler.checkUser(user=checkUser)
        return check
