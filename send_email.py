from __future__ import print_function
import base64
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

"""
send_message: function

parameters:

    receiver: email address of the recipient
    subject: email subject
    content: email body
    pdfs: list of pdfs that are sent to the receiver, the input should be the path of the pdf/s enclosed in brackets 
    images: list of images that are sent to the receiver, the input should be the path of the image/s enclosed in brackets

returns: the message

"""

def send_message(receiver, subject, content, pdfs : list = None, images : list = None, cc = None, classification = None):

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
                    img.add_header('Content-Disposition', 'attachment', filename = "qr.png")
                    message.attach(img)

        if pdfs: 
            for pdf in pdfs: 
                with open(pdf, 'rb') as content_file:
                    file = MIMEApplication(content_file.read())
                    file.add_header('Content-Disposition', 'attachment', filename = "receipt.pdf" if (classification == "receipt") else "invoice.pdf")
                    message.attach(file)

        create_message = {
            'raw': base64.urlsafe_b64encode(bytes(message.as_string(), "utf-8")).decode("utf-8")
        }

        send_message = service.users().messages().send(userId = "me", body = create_message).execute()

    except HttpError as error:
    
        send_message = None
    
    return send_message

