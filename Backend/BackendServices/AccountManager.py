import mysql
import json
from DatabaseHandler.User import User
from DatabaseHandler.DatabaseHandler import DatabaseHandler


class AccountManager:
    '''
    Class for handling Account Data
    '''
    def __init__(self):
        '''

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

        :param UserID:
        :param Firstname:
        :param Lastname:
        :param Username:
        :param Email:
        :param Password:
        :param IsConfirmed:
        :return:
        '''
        newUser = User(UserID, Firstname, Lastname, Username, Email, Password, IsConfirmed)
        # sendRegistrationEmail()
        checkMethod = self.mDBHandler.registerUser(newUser)
        if checkMethod:
            return True
        else:
            return False

    def sendRegistrationEmail(self, UserID: str):
        '''

        :param UserID:
        :return:
        '''
        return

    def checkLoginCredeantials(self, Username: str, Password: str):
        '''

        :param Username:
        :param Password:
        :return:
        '''
        checkUser = User(userName=Username, password=Password)
        returnedUser = self.mDBHandler.loginUser(checkUser)
        if returnedUser:
            response = {
                'username': returnedUser.userName,
                'userID': returnedUser.userID
            }
            return response
            #self.wfile.write(json.dumps(response).encode(encoding='utf_8'))
        #else:
            #self._set_response(400)


    def sendPasswordResetEmail(self, UserID: str):
        '''

        :param UserID:
        :return:
        '''
        return

    def changePasswordInDatabase(self, UserID: str, Password: str):
        '''

        :param UserID:
        :param Password:
        :return:
        '''
        return

    def deleteUser(self, UserID: str):
        '''

        :param UserID:
        :return:
        '''
        self.mDBHandler.deleteUserByID(UserID)
        return True

    def createRegistrationToken(self, UserID: str) -> str:
        '''

        :param UserID:
        :return:
        '''
        return
