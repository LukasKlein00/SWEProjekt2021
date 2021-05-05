import smtplib
import ssl
from email.message import EmailMessage
from EmailServices.MessageType import MessageType
from EmailServices.FileReader import FileReader
import socket


class EmailSender:
    """Basic class for interaction to User via email"""
    def __init__(self, user_email, user_id: str):
        """
        Constructor for email Sender to initiate needed parameters
        
        :param user_email: email of the recipient - String
        :param token: Token to verify User after email confirmation - String
        """
        self.user_email = user_email
        self.msg = EmailMessage()
        self.user_id = user_id
        self.e_mail = "mudcakegame@gmail.com"

    def __send_via_server_context(self, msg: EmailMessage):
        """Method to send emails via google gMail

        :param msg: preconfigured message in external method - EmailMessage
        """
        print("email send to:" + msg['To'])
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
            server.login(self.e_mail, bytes(b'$9PLnJ5NsB#!').decode('utf8', 'strict'))
            server.send_message(msg)

    def send_email(self, m_type: MessageType):
        """Prepares email with given context and initializes sending

        :param m_type: type of message to be send - MessageType
        """
        host_name = socket.gethostname()
        local_ip = socket.gethostbyname(host_name)
        print(local_ip)

        if m_type == MessageType.registration:
            content_reader = FileReader("EmailServices/confirmationEmailTemplates/content")
            content = content_reader.read()
            host_name = socket.gethostname()

            if str(socket.gethostbyname(host_name)) != "193.196.53.67":
                content = content.replace("{Server}", "localhost:4200")
            else:
                content = content.replace("{Server}", "193.196.54.98")

            self.msg.set_content(content.replace("{UserToken}", self.user_id))
            self.msg["Subject"] = content_reader.overwrite_name("EmailServices/confirmationEmailTemplates/subject").read()
            self.msg["From"] = self.e_mail
            self.msg["To"] = self.user_email
            self.__send_via_server_context(self.msg)

        if m_type == MessageType.reset_password:
            content_reader = FileReader("EmailServices/resetPasswordEmailTemplates/content")
            content = content_reader.read()
            host_name = socket.gethostname()

            if str(socket.gethostbyname(host_name)) != "193.196.53.67":
                content = content.replace("{Server}", "localhost:4200")
            else:
                content = content.replace("{Server}", "193.196.54.98")

            self.msg.set_content(content.replace("{UserToken}", str(self.user_id)))
            self.msg["Subject"] = content_reader.overwrite_name(
                "EmailServices/resetPasswordEmailTemplates/subject").read()
            self.msg["From"] = self.e_mail
            self.msg["To"] = self.user_email
            self.__send_via_server_context(self.msg)
