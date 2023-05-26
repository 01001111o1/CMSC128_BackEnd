from flask import render_template, request, redirect, jsonify, make_response, url_for, session, flash, Blueprint, jsonify
from flask_login import login_required, current_user
from . import db
from app import app, executor
from .models import Request
from .email_template import request_approved_template, documents_approved_template, documents_available_template
import shutil

from datetime import date

from docxtpl import DocxTemplate
from docx2pdf import convert
import ast 

from send_email import send_message

from .Lists import Documents

import pythoncom

from .send_generated_files import background_runner

from flask_paginate import Pagination

admin_views = Blueprint('admin_views', __name__)

@admin_views.route("/admin/dashboard")
@login_required
def admin_dashboard():
    page = int(request.args.get('page', 1))
    requests = Request.query.order_by(Request.queue_number)
    pages = requests.paginate(page = page, per_page = app.config['REQUESTS_PER_PAGE']) 

    return render_template("admin/dashboard.html", pages = pages, documents = Documents, user = current_user)

@admin_views.route("/sort/<parameter>")
@login_required
def sort(parameter):
    if parameter == "desc":
        requests = Request.query.order_by(Request.date_of_request.desc())
    elif parameter == "asc":
        requests = Request.query.order_by(Request.date_of_request)
    else:
        requests = Request.query.filter(Request.requested_documents.contains(parameter))

    pages = requests.paginate(page = 1, per_page = app.config['REQUESTS_PER_PAGE']) 

    return render_template("admin/dashboard.html", pages = pages, documents = Documents, user = current_user)

@admin_views.route("/update/<int:queue_number>/<classification>")
@login_required
def update(queue_number, classification):
    query = Request.query.get_or_404(queue_number)  
    try:
        if classification == "request_approved":
            send_message("scvizconde@up.edu.ph", 
                query.email, 
                f"Request approved for order number { query.queue_number }", 
                request_approved_template(query.first_name, query.queue_number))
            query.request_approved = True
        elif classification == "documents_approved":
            send_message("scvizconde@up.edu.ph", 
                query.email, 
                f"Documents approved for order number { query.queue_number }", 
                documents_approved_template(query.first_name, query.queue_number))
            query.documents_approved = True
        elif classification == "claiming_available":
            send_message("scvizconde@up.edu.ph", 
                query.email, 
                f"order number { query.queue_number } available for claiming", 
                documents_available_template(query.first_name, query.queue_number))
            query.request_available = True
        else:
            query.request_paid = True
        db.session.commit()
        flash("Successfully sent update email", "success")
        return redirect(url_for("admin_views.admin_dashboard"))
    except:
        flash("error sending update email", "error")
        return redirect(url_for("admin_views.admin_dashboard"))

@admin_views.route("/delete/<int:queue_number>")
@login_required
def delete_entry(queue_number):
    try:
        query = Request.query.get_or_404(queue_number)  
        folder_name =" ".join([query.first_name.upper(), query.middle_name.upper(), query.last_name.upper()])
        folder_path = app.config["FILE_UPLOADS"] + "/" + folder_name
        
        background_runner.send_email_async(queue_number)

        shutil.rmtree(folder_path, ignore_errors = False)

        db.session.delete(query)
        db.session.commit()
        flash("Transaction successfully deleted", "success")
        return redirect(url_for("admin_views.admin_dashboard"))
    except:
        flash("Error deleting transaction", "error")
        return redirect(url_for("admin_views.admin_dashboard"))

@admin_views.route("/remove/<int:queue_number>")
@login_required
def remove_entry(queue_number):
    query = Request.query.get_or_404(queue_number)  
    folder_name =" ".join([query.first_name.upper(), query.middle_name.upper(), query.last_name.upper()])
    folder_path = app.config["FILE_UPLOADS"] + "/" + folder_name

    try:
        shutil.rmtree(folder_path, ignore_errors = False)

        db.session.delete(query)
        db.session.commit()
        flash("Entry successfully deleted", "success")
        return redirect(url_for("admin_views.admin_dashboard"))
    except:
        flash("Error deleting transaction", "error")
        return redirect(url_for("admin_views.admin_dashboard"))


