from __future__ import print_function

import base64
from email.message import EmailMessage

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

#NOTE: SENDER EMAIL IS THE ONE YOU USED TO CREATE THE PROJECT IN GOOGLE CLOUSPACE!!!!!

def send_message(receiver, subject, content, pdfs : list = None, images : list = None,  cc = None):

    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    try:
        service = build('gmail', 'v1', credentials = creds)
        
        message = MIMEMultipart()
        message['To'] = receiver
        message['Subject'] = subject
        message['cc'] = cc

        message_text = MIMEText(content, 'html')
        message.attach(message_text)

        if images:
            for image in images:
                with open(image, 'rb') as content_image:
                    img = MIMEImage(content_image.read())
                    img.add_header('Content-Disposition', 'attachment', filename = "invoice.jpg")
                    message.attach(img)

        if pdfs: 
            for pdf in pdfs: 
                with open(pdf, 'rb') as content_file:
                    file = MIMEApplication(content_file.read())
                    file.add_header('Content-Disposition', 'attachment', filename = "invoice.pdf")
                    message.attach(file)

        create_message = {
            'raw': base64.urlsafe_b64encode(bytes(message.as_string(), "utf-8")).decode("utf-8")
        }

        send_message = service.users().messages().send(userId="me", body = create_message).execute()
    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None
    return send_message


