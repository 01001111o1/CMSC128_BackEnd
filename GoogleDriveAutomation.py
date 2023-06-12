from __future__ import print_function
import pickle
import os
import os.path
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from flask import session

SCOPES = ['https://www.googleapis.com/auth/drive']

def retrieve_drive_data():

    creds = None

    if os.path.exists('token_drive.json'):
        creds = Credentials.from_authorized_user_file('token_drive.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token_drive.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)
    
    folderId = "1ot13ep8FeYMq3v10a27uIpuOFgg-8JJN"  
    destinationFolder = "C:/Users/Sean/Desktop/CMSC128Project/Payments"

    downloadFolder(service, folderId, destinationFolder)

def downloadFolder(service, fileId, destinationFolder):
    
    if not os.path.isdir(destinationFolder):
        os.mkdir(path = destinationFolder)

    results = service.files().list( q = "parents in '{0}'".format(fileId), fields="files(id, name, mimeType)" ).execute()

    items = results.get('files', [])
    
    with open('payment_list.txt', 'w') as f:

        for item in items:
            itemName = item['name']
            itemId = item['id']
            itemType = item['mimeType']
            filePath = destinationFolder + "/" + itemName

            if os.path.isdir(filePath):
                continue

            if itemType == 'application/vnd.google-apps.folder':
                f.write(itemName)
                f.write("\n")
                downloadFolder(service, itemId, filePath)
            else:
                downloadFile(service, itemId, filePath)
 
def downloadFile(service, fileId, filePath):

    request = service.files().get_media(fileId=fileId)
    fh = io.FileIO(filePath, mode='wb')
    
    try:
        downloader = MediaIoBaseDownload(fh, request, chunksize = 1048576 * 1048576)

        done = False
        while done is False:
            status, done = downloader.next_chunk(num_retries = 2)
    finally:
        fh.close()

