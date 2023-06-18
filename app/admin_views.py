"""

File contains the routes that are accessible from the admin side (login required)

2023 UPB2GO

"""

from flask import render_template, request, redirect, jsonify, make_response, url_for, session, flash, Blueprint, jsonify
from flask_login import login_required, current_user
from . import db
from app import app, executor, scheduler
from .models import Request
from .email_template import email_template
import shutil
import time
from datetime import date
import ast 
from send_email import send_message
from .Lists import Documents
import pythoncom
from .background_runner import background_runner
from flask_paginate import Pagination
from werkzeug.test import create_environ
from werkzeug.urls import iri_to_uri
from werkzeug.wsgi import get_current_url
from sqlalchemy.orm.exc import NoResultFound
from payment_processing import payment_received
from datetime import datetime
import pytz
import os.path

admin_views = Blueprint('admin_views', __name__)

"""
Route that displays the admin login page (only page that doesnt require logging in)

"""
@admin_views.route("/admin/login")
def admin_login():
    return render_template("admin/admin-login.html", user = current_user)
"""

Route that displays the admin dashboard

Implements pagnination to prevent the server from accessing all records at once and instead displays only a fixed number (5) of entries at a time

a url is stored in the session variable to maintain the current page and sort criteria on change / update

In the case where an entry is rejected for some reason, a POST request is sent to this route and is processed by sending an email which contains
the reaosn for rejecting said entry and deleting it from the database as well as removing the folder from the server's storage

"""
@admin_views.route("/admin/dashboard/<parameter>/", methods = ["GET", "POST"])
@login_required
def admin_dashboard(parameter):

    page = int(request.args.get('page', 1))

    background_runner.payment_received_asynch()

    env = create_environ(f"?page={page}", f"http://127.0.0.1:5000/admin/dashboard/{parameter}")
    session["url"] = iri_to_uri(get_current_url(env))

    if parameter == "default":
        requests = Request.query.order_by(Request.queue_number)
    elif parameter == "desc":
        requests = Request.query.order_by(Request.date_of_request.desc())
    elif parameter == "asc":
        requests = Request.query.order_by(Request.date_of_request)
    elif parameter == "payment_desc":
        requests = Request.query.order_by(Request.payment_date.desc())
    elif parameter == "payment_asc":
        requests = Request.query.order_by(Request.payment_date)
    else:
        requests = Request.query.filter(Request.requested_documents.contains(parameter))

    pages = requests.paginate(page = page, per_page = app.config['REQUESTS_PER_PAGE']) 

    if request.method == "POST":
        reason = request.form.get("reason_reject")
        queue_number = request.form.get("id_to_remove")
        query = Request.query.get_or_404(queue_number)  

        subject, content = email_template(query.first_name, queue_number, "request_rejected", reason)
        background_runner.send_message_asynch(query.email, subject, content)

        remove_entry(queue_number)

        return redirect(session["url"])

    return render_template("admin/dashboard.html", pages = pages, documents = Documents, user = current_user, parameter = parameter)

"""
Route that handles any changes to any toggle-able part of the dashboard

Any click event to one of these toggle-able elements is handled accordingly and an appropriate email is sent to the requester for a specific entry
"""
@admin_views.route("/update/<int:queue_number>/<classification>")
@login_required
def update(queue_number, classification):
    query = Request.query.get_or_404(queue_number)  
    subject, content = email_template(query.first_name, queue_number, classification)

    try:
        if classification == "documents_approved":
            background_runner.send_message_asynch(query.email, subject, content, None, [app.config["QR_CODE_PATH"]])
        else:
            background_runner.send_message_asynch(query.email, subject, content)

        exec(f'query.{classification} = True')

        if classification == "request_paid" and query.payment_date is None: 
            query.payment_date = datetime.now(pytz.timezone('Singapore')).replace(microsecond = 0)

        db.session.commit()
        flash("Successfully sent update email", "success")
        return redirect(session["url"])
    except:
        flash("error sending update email", "error")
        return redirect(session["url"])


"""
Route that handles the case where a transaction is finished (has been claimed)

An email containing the receipt of the transaction is sent to the requester.

"""
@admin_views.route("/delete/<int:queue_number>")
@login_required
def delete_entry(queue_number):
    try:

        background_runner.send_invoice_or_receipt_asynch(queue_number, "receipt")

        remove_entry(queue_number)

        flash("Transaction successfully deleted", "success")
        return redirect(session["url"])
    except:
        flash("Error deleting transaction", "error")
        return redirect(session["url"])

"""
remove_entry: function

parameter: queue_number

Removes the entry from the database as well as any folders associated with that entry

"""
def remove_entry(queue_number):
    query = Request.query.get_or_404(queue_number)  
    folder_name = " ".join([query.first_name.upper(), query.middle_name.upper(), query.last_name.upper()])
    folder_path = app.config["FILE_UPLOADS"] + "/" + folder_name
    payment_path = app.config["PAYMENT_UPLOADS"] + "/" + str(queue_number)

    if os.path.isdir(payment_path):
        shutil.rmtree(payment_path)

    if os.path.isdir(folder_path):
        shutil.rmtree(folder_path)
        
    db.session.delete(query)
    db.session.commit()
    flash("Entry successfully deleted", "success")
    return redirect(session["url"])


