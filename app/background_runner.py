"""

File that contains all functions that runs asynchronously
Processes are explained in each of their synchronous counterparts.

2023 UPB2GO

"""

from app import app, executor
from .models import Request
from datetime import date
from docxtpl import DocxTemplate
from docx2pdf import convert
import ast 
from send_email import send_message
from GoogleDriveAutomation import retrieve_drive_data
from payment_processing import payment_received
from .send_templated_documents import send_invoice_or_receipt
import pythoncom
from flask_executor import Executor
import uuid
import shutil
import os
from flask import session

class BackgroundRunner: 
    def __init__(self, executor):
        self.executor = executor

    def send_invoice_or_receipt_asynch(self, queue_number, classification):
        task_id = uuid.uuid4().hex
        self.executor.submit_stored(task_id, send_invoice_or_receipt, queue_number, classification)
        return task_id

    def send_message_asynch(self, receiver, subject, content, pdfs : list = None, images : list = None,  cc = None):
        task_id = uuid.uuid4().hex
        self.executor.submit_stored(task_id, send_message, receiver, subject, content, pdfs, images, cc)
        return task_id

    def retrieve_drive_data_asynch(self):
        task_id = uuid.uuid4().hex
        self.executor.submit_stored(task_id, retrieve_drive_data)
        return task_id

    def payment_received_asynch(self):
        task_id = uuid.uuid4().hex
        self.executor.submit_stored(task_id, payment_received)
        return task_id     

    def task_status(self, task_id):
        if not executor.futures.done(task_id):
            return "running"
        else:
            return "completed"

background_runner = BackgroundRunner(executor)
