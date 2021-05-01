import mysql
import json
from DatabaseHandler.User import User
from DatabaseHandler.DatabaseHandler import DatabaseHandler


class AccountManager:
    def __init__(self):
        self.mDBHandler = DatabaseHandler(mysql.connector.connect(
            host="193.196.53.67",
            port="1189",
            user="jack",
            password="123123"
        ))

    def registerUser(self, UserID: str, Firstname: str, Lastname: str, Username: str, Email: str, Password: str,
                     IsConfirmed: bool) -> bool:
        newUser = User(UserID, Firstname, Lastname, Username, Email, Password, IsConfirmed)
        # sendRegistrationEmail()
        checkMethod = self.mDBHandler.registerUser(newUser)
        if checkMethod:
            return True
        else:
            return False

    def sendRegistrationEmail(UserID: int):
        return

    def checkLoginCredeantials(self, Username: str, Password: str):
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


    def sendPasswordResetEmail(UserID: int):
        return

    def changePasswordInDatabase(UserID: int, Password: str):
        return

    def deleteUser(UserID: int):
        return

    def createRegistrationToken(UserID: int) -> str:
        return
