import smtplib
import ssl
from email.message import EmailMessage
from Backend.EmailServices.messageType import messageType
from Backend.EmailServices.fileReader import fileReader


class EmailSender:
    def __init__(self, userEmail, token: str = None):
        self.userEmail = userEmail
        self.token = token
        self.msg = EmailMessage()
        self.email = "mudcakegame@gmail.com"

    def __sendViaServerContext(self, msg: EmailMessage):
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
            server.login(self.email, bytes(b'$9PLnJ5NsB#!').decode('utf8', 'strict'))
            server.send_message(msg)

    def sendEmail(self, mType: messageType):
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
