import smtplib
import ssl
from email.message import EmailMessage
from Backend.EmailServices.messageType import messageType
from Backend.EmailServices.fileReader import fileReader


class EmailSender:
    """Basic class for interaction to User via Email"""
    def __init__(self, userEmail, token: str = None):
        """Constructor for Email Sender to initiate needed parameters

        :param userEmail: Email of the recipient - String
        :param token: Token to verify User after email confirmation - String
        """
        self.userEmail = userEmail
        self.token = token
        self.msg = EmailMessage()
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
        if mType == messageType.registration:
            contentReader = fileReader("confirmationEmailTemplates/content")
            self.msg.set_content(contentReader.read())
            self.msg["Subject"] = contentReader.overwriteName("confirmationEmailTemplates/subject").read()
            self.msg["From"] = self.email
            self.msg["To"] = self.userEmail
            self.__sendViaServerContext(self.msg)

        if mType == messageType.resetPassword:
            contentReader = fileReader("resetPasswordEmailTemplates/content")
            self.msg.set_content(contentReader.read())
            self.msg["Subject"] = contentReader.overwriteName("resetPasswordEmailTemplates/subject").read()
            self.msg["From"] = self.email
            self.msg["To"] = self.userEmail
            self.__sendViaServerContext(self.msg)
