from app import app, executor
from .models import Request

from datetime import date

from docxtpl import DocxTemplate
from docx2pdf import convert
import ast 

from send_email import send_message
from GoogleDriveAutomation import retrieve_drive_data

from payment_processing import payment_received

import pythoncom

from flask_executor import Executor
import uuid

import shutil
import os

from flask import session

class BackgroundRunner: 
    def __init__(self, executor):
        self.executor = executor

    def send_invoice_or_receipt(self, queue_number, classification):

        query = Request.query.get_or_404(queue_number)
        requester_name = " ".join([query.first_name.upper(), query.middle_name.upper(), query.last_name.upper()])  
        folder_name = " ".join([query.first_name.upper(), query.middle_name.upper(), query.last_name.upper(), classification.upper()])
        folder_path = app.config["FILE_UPLOADS"] + "/" + folder_name

        os.mkdir(folder_path)

        price_map = query.price_map
        price_dictionary = ast.literal_eval(price_map)

        invoice_list = [[1, k, int(v)] for k, v in price_dictionary.items()]

        if classification == "receipt":
            doc = DocxTemplate("app/receipt_template.docx")
        else:
            doc = DocxTemplate("app/invoice_template.docx")

        doc.render({
            "name" : requester_name,
            "student_number" : query.student_number,
            "scholar" : "Yes" if "For Scholarship" in query.remarks else "No",
            "date" : date.today(),
            "invoice_list" : invoice_list,
            "total" : sum(v[2] for v in invoice_list)
        })

        docxpath = folder_path + "/" + query.last_name + ".docx"
        pdfpath = folder_path + "/" + query.last_name + ".pdf"
        doc.save(docxpath)
        pythoncom.CoInitialize()
        convert(docxpath, pdfpath)

        send_message(query.email, 
                    f'{classification} for order number {query.queue_number}', 
                    f"Good Day, Here is your {classification} for order number {query.queue_number}", 
                    [pdfpath])

        shutil.rmtree(folder_path, ignore_errors = False)

        return None

    def send_invoice_or_receipt_asynch(self, queue_number, classification):
        task_id = uuid.uuid4().hex
        self.executor.submit_stored(task_id, self.send_invoice_or_receipt, queue_number, classification)
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
