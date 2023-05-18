from __future__ import print_function

import base64
from email.message import EmailMessage

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials

from email.mime.text import MIMEText


SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def send_message(sender, receiver, subject, content, cc = None):

    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    try:
        service = build('gmail', 'v1', credentials = creds)
        message = MIMEText(content, 'plain')

        message['To'] = receiver
        message['From'] = sender
        message['Subject'] = subject
        message['cc'] = cc

        encoded_message = base64.urlsafe_b64encode(bytes(message.as_string(), "utf-8")).decode("utf-8")
        create_message = {
            'raw': encoded_message
        }

        send_message = service.users().messages().send(userId="me", body=create_message).execute()
    except HttpError as error:
        print(F'An error occurred: {error}')
        send_message = None
    return send_message

