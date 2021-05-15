#!/usr/bin/env python
__author__ = "Lukas Klein & Thomas Zimmermann"
__copyright__ = "Copyright 2021, The MUDCake Project"
__credits__ = "Hauke Presig, Jack Drillisch, Jan Gruchott, Lukas Klein, Robert Fendrich, Thomas Zimmermann"

__license__ = """MIT License

                     Copyright (c) 2021 MUDCake Project

                     Permission is hereby granted, free of charge, to any person obtaining a copy
                     of this software and associated documentation files (the "Software"), to deal
                     in the Software without restriction, including without limitation the rights
                     to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
                     copies of the Software, and to permit persons to whom the Software is
                     furnished to do so, subject to the following conditions:

                     The above copyright notice and this permission notice shall be included in all
                     copies or substantial portions of the Software.

                     THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
                     IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
                     FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
                     AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
                     LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
                     OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
                     SOFTWARE."""

__version__ = "1.0.0"
__maintainer__ = "Lukas Klein & Thomas Zimmermann"
__email__ = "mudcake@gmail.com"
__status__ = "Development"

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
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=ssl.create_default_context()) as server:
            server.login(self.e_mail, bytes(b'$9PLnJ5NsB#!').decode('utf8', 'strict'))
            server.send_message(msg)

    def send_email(self, m_type: MessageType):
        """Prepares email with given context and initializes sending

        :param m_type: type of message to be send - MessageType
        """
        host_name = socket.gethostname()
        local_ip = socket.gethostbyname(host_name)

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
