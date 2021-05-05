import smtplib
import ssl
from email.message import EmailMessage
from EmailServices.messageType import messageType
from EmailServices.fileReader import fileReader
import socket


class EmailSender:
    """Basic class for interaction to User via email"""
    def __init__(self, user_email, user_id: str):
        """
        Constructor for email Sender to initiate needed parameters
        
        :param user_email: email of the recipient - String
        :param token: Token to verify User after email confirmation - String
        """
        self.userEmail = user_email
        self.msg = EmailMessage()
        self.userID = user_id
        self.email = "mudcakegame@gmail.com"

    def __send_via_server_context(self, msg: EmailMessage):
        """Method to send emails via google gMail

        :param msg: preconfigured message in external method - EmailMessage
        """
        print("email send to:" + msg['To'])
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
            server.login(self.email, bytes(b'$9PLnJ5NsB#!').decode('utf8', 'strict'))
            server.send_message(msg)

    def send_email(self, m_type: messageType):
        """Prepares email with given context and initializes sending

        :param m_type: type of message to be send - MessageType
        """
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(local_ip)

        if m_type == messageType.registration:
            content_reader = fileReader("EmailServices/confirmationEmailTemplates/content")
            content = content_reader.read()
            hostname = socket.gethostname()

            if str(socket.gethostbyname(hostname)) != "193.196.53.67":
                content = content.replace("{Server}", "localhost:4200")
            else:
                content = content.replace("{Server}", "193.196.54.98")

            self.msg.set_content(content.replace("{UserToken}", self.userID))
            self.msg["Subject"] = content_reader.overwrite_name("EmailServices/confirmationEmailTemplates/subject").read()
            self.msg["From"] = self.email
            self.msg["To"] = self.userEmail
            self.__send_via_server_context(self.msg)

        if m_type == messageType.reset_password:
            content_reader = fileReader("EmailServices/resetPasswordEmailTemplates/content")
            content = content_reader.read()
            hostname = socket.gethostname()

            if str(socket.gethostbyname(hostname)) != "193.196.53.67":
                content = content.replace("{Server}", "localhost:4200")
            else:
                content = content.replace("{Server}", "193.196.54.98")

            self.msg.set_content(content.replace("{UserToken}", str(self.userID)))
            self.msg["Subject"] = content_reader.overwrite_name(
                "EmailServices/resetPasswordEmailTemplates/subject").read()
            self.msg["From"] = self.email
            self.msg["To"] = self.userEmail
            self.__send_via_server_context(self.msg)
