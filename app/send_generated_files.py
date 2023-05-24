from app import app, executor
from .models import Request

from datetime import date

from docxtpl import DocxTemplate
from docx2pdf import convert
import ast 

from send_email import send_message

import pythoncom

from flask_executor import Executor
import uuid4

class BackgroundRunner: 
    def __init__(self, executor):
        self.executor = executor

    def send_invoice_or_receipt(self, queue_number):
        query = Request.query.get_or_404(queue_number)  
        folder_name =" ".join([query.first_name.upper(), query.middle_name.upper(), query.last_name.upper()])
        folder_path = app.config["FILE_UPLOADS"] + "/" + folder_name

        price_map = query.price_map
        price_dictionary = ast.literal_eval(price_map)

        invoice_list = [[1, k, int(v)] for k, v in price_dictionary.items()]
        
        doc = DocxTemplate("app/invoice_template.docx")

        doc.render({
            "name" : folder_name,
            "student_number" : query.student_number,
            "date" : date.today(),
            "invoice_list" : invoice_list,
            "total" : sum(v[2] for v in invoice_list)
        })

        docxpath = folder_path + "/" + query.last_name + ".docx"
        pdfpath = folder_path + "/" + query.last_name + ".pdf"
        doc.save(docxpath)
        pythoncom.CoInitialize()
        convert(docxpath, pdfpath)

        send_message("scvizconde@up.edu.ph", 
                    query.email, 
                    f'Receipt for order number {query.queue_number}', 
                    "test content", 
                    [pdfpath])
        return None

    def send_email_async(self, queue_number):
        task_id = uuid.uuid4().hex
        self.executor.submit_stored(task_id, self.send_invoice_or_receipt, queue_number)
        return task_id

background_runner = BackgroundRunner(executor)
