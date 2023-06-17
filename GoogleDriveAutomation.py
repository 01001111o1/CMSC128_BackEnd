from __future__ import print_function
import os
import os.path
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from flask import session
from app import models

SCOPES = ['https://www.googleapis.com/auth/drive']

"""
retrieve_drive_data : function

Initializes credentials which is stored in a json file to prevent reauthenticating every time the app is ran.
Recursively downloads folders and subfolders within the parent directory and deletes them afterwards. 
Deleting folders is commented out since the extension to map google forms google drive has a per month quota
"""
def retrieve_drive_data():

    creds = Credentials.from_authorized_user_file('token_drive.json', SCOPES)

    service = build('drive', 'v3', credentials = creds)
    
    folderId = "1ot13ep8FeYMq3v10a27uIpuOFgg-8JJN"  
    FolderPath = "C:/Users/Sean/Desktop/CMSC128Project/Payments"

    downloadFolder(service, folderId, FolderPath)
    #delete_folder_contents(service, folderId) #Commented out to preserve the 25 per month gform -> gdrive limit using Form Director plugin 

"""
delete_folder_contents : function

parameters: 
    service
        initializes the communication between the application and the API
    folderID
        folderID of the parent folder
    FolderPath
        Path of where to download the files from google drive

deletes folders from inside a parameterized google drive folder ID. No need for this function to run recursively as we only need to look at the inital level of subfolders
and delete them and it will cascade into their own subfolders and files.
"""
def delete_folder_contents(service, fileId):
    
    results = service.files().list( q = f"parents in '{fileId}'", fields="files(id, name, mimeType)" ).execute()
    items = results.get('files', [])
    
    for item in items:
        itemId = item['id']
        itemType = item['mimeType']

        if itemType == 'application/vnd.google-apps.folder':
            service.files().delete(fileId = itemId).execute()     

"""
downloadFolder : function

parameters: 
    service
        initializes the communication between the application and the API
    folderID
        folderID of the parent folder
    FolderPath
        Path of where to download the files from google drive

Creates a folder in the server if it doesnt exist yet and checks the type of file we are currently on. If it is a folder it keeps track of the file
name to be used for requesting data from the database.
"""
def downloadFolder(service, fileId, FolderPath):
    
    if not os.path.isdir(FolderPath):
        os.mkdir(FolderPath)

    results = service.files().list( q = f"parents in '{fileId}'", fields="files(id, name, mimeType)" ).execute()

    items = results.get('files', [])
    
    with open('payment_list.txt', 'w') as f:

        for item in items:
            itemName = item['name']
            itemId = item['id']
            itemType = item['mimeType']
            filePath = FolderPath + "/" + itemName

            if os.path.isdir(filePath):
                continue

            if itemType == 'application/vnd.google-apps.folder':
                if models.Request.query.get(itemName) is not None:
                    f.write(itemName)
                    f.write("\n")
                    downloadFolder(service, itemId, filePath)
            else:
                downloadFile(service, itemId, filePath)

"""
downloadFile : function

parameters: 
    service
        initializes the communication between the application and the API
    folderID
        folderID of the parent folder
    FolderPath
        Path of where to download the files from google drive

Downloads the PDF content of a folder
"""
def downloadFile(service, fileId, filePath):

    request = service.files().get_media(fileId = fileId)
    fh = io.FileIO(filePath, mode = 'wb')
    
    try:
        downloader = MediaIoBaseDownload(fh, request, chunksize = 1048576 * 1048576)

        done = False
        while done is False:
            status, done = downloader.next_chunk(num_retries = 2)
    finally:
        fh.close()

