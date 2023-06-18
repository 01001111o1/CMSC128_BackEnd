from app import app
from .models import Request
from datetime import date
from docxtpl import DocxTemplate
from docx2pdf import convert
import ast 
from send_email import send_message
import pythoncom
import shutil
import os
import os.path


"""
send_invoice_or_receipt: function

parameters:
    queue_number
        Queue number of the person to be sent the invoice / receipt to. Is used to retrieve relevant information from the database to put into the template
    classification
        The type of pdf that will be sent is dependent on the classifation whether it is "invoice" or "receipt"

returns: None

Requester data is retrieved from the database and is inserted into a templated Microsoft Word Document which is then converted into a PDF
and sent asynchronously to his / her email.

"""
def send_invoice_or_receipt(queue_number, classification):

    query = Request.query.get_or_404(queue_number)
    requester_name = " ".join([query.first_name.upper(), query.middle_name.upper(), query.last_name.upper()])  
    folder_name = " ".join([requester_name, classification.upper()])
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
