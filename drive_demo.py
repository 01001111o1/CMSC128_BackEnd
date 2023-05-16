from __future__ import print_function

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from Google import Create_Service

CLIENT_SECRET_FILE = 'client_oauth.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

def search_folder(target):

    try:
        files = []
        page_token = None
        while True:
            response = service.files().list(q="name = '"+ target +"' and mimeType = 'application/vnd.google-apps.folder'", spaces='drive', fields='nextPageToken, files(id, name)', pageToken=page_token).execute()
            for file in response.get('files', []):
                print(F'Found file: {file.get("name")}, {file.get("id")}')
            files.extend(response.get('files', []))
            page_token = response.get('nextPageToken', None)
            if page_token is None:
                break

    except HttpError as error:
        print(F'An error occurred: {error}')
        files = None

    return files[0]["id"]
