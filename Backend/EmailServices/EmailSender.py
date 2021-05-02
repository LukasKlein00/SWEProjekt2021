import smtplib
import ssl
from email.message import EmailMessage
from EmailServices.messageType import messageType
from EmailServices.fileReader import fileReader
import socket


class EmailSender:
    """Basic class for interaction to User via Email"""
    def __init__(self, userEmail, userID: str):
        """Constructor for Email Sender to initiate needed parameters

        :param userEmail: Email of the recipient - String
        :param token: Token to verify User after email confirmation - String
        """
        self.userEmail = userEmail
        self.msg = EmailMessage()
        self.userID = userID
        self.email = "mudcakegame@gmail.com"

    def __sendViaServerContext(self, msg: EmailMessage):
        """Method to send emails via google gMail

        :param msg: preconfigured message in external method - EmailMessage
        """
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
            server.login(self.email, bytes(b'$9PLnJ5NsB#!').decode('utf8', 'strict'))
            server.send_message(msg)

    def sendEmail(self, mType: messageType):
        """Prepares email with given context and initializes sending

        :param mType: type of message to be send - MessageType
        """
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(local_ip)

        if mType == messageType.registration:
            contentReader = fileReader("EmailServices/confirmationEmailTemplates/content")
            content = contentReader.read()
            hostname = socket.gethostname()

            if str(socket.gethostbyname(hostname)) != "193.196.53.67":
                content = content.replace("{Server}", "localhost:4200")
            else:
                content = content.replace("{Server}", "193.196.54.98")

            self.msg.set_content(content.replace("{UserToken}", self.userID))
            self.msg["Subject"] = contentReader.overwriteName("EmailServices/confirmationEmailTemplates/subject").read()
            self.msg["From"] = self.email
            self.msg["To"] = self.userEmail
            self.__sendViaServerContext(self.msg)

        if mType == messageType.resetPassword:
            contentReader = fileReader("EmailServices/resetPasswordEmailTemplates/content")
            self.msg.set_content(contentReader.read())
            self.msg["Subject"] = contentReader.overwriteName("EmailServices/resetPasswordEmailTemplates/subject").read()
            self.msg["From"] = self.email
            self.msg["To"] = self.userEmail
            self.__sendViaServerContext(self.msg)
