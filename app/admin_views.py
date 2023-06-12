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

from .send_generated_files import background_runner

from flask_paginate import Pagination

from werkzeug.test import create_environ
from werkzeug.urls import iri_to_uri
from werkzeug.wsgi import get_current_url

from sqlalchemy.orm.exc import NoResultFound

from payment_processing import payment_received

admin_views = Blueprint('admin_views', __name__)

@admin_views.route("/admin/login")
def admin_login():
    return render_template("admin/admin-login.html", user = current_user)

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

@admin_views.route("/update/<int:queue_number>/<classification>")
@login_required
def update(queue_number, classification):
    query = Request.query.get_or_404(queue_number)  
    try:
        subject, content = email_template(query.first_name, queue_number, classification)
        background_runner.send_message_asynch(query.email, subject, content)

        exec(f'query.{classification} = True')

        db.session.commit()
        flash("Successfully sent update email", "success")
        return redirect(session["url"])
    except:
        flash("error sending update email", "error")
        return redirect(session["url"])

@admin_views.route("/delete/<int:queue_number>")
@login_required
def delete_entry(queue_number):
    try:
        query = Request.query.get_or_404(queue_number)  
        folder_name =" ".join([query.first_name.upper(), query.middle_name.upper(), query.last_name.upper()])
        folder_path = app.config["FILE_UPLOADS"] + "/" + folder_name

        background_runner.send_invoice_or_receipt_asynch(queue_number, "receipt")

        db.session.delete(query)
        db.session.commit()
        
        shutil.rmtree(folder_path)

        flash("Transaction successfully deleted", "success")
        return redirect(session["url"])
    except:
        flash("Error deleting transaction", "error")
        return redirect(session["url"])

@admin_views.route("/remove/<int:queue_number>")
@login_required
def remove_entry(queue_number):
    query = Request.query.get_or_404(queue_number)  
    folder_name = " ".join([query.first_name.upper(), query.middle_name.upper(), query.last_name.upper()])
    folder_path = app.config["FILE_UPLOADS"] + "/" + folder_name

    try:
        shutil.rmtree(folder_path, ignore_errors = False)

        db.session.delete(query)
        db.session.commit()
        flash("Entry successfully deleted", "success")
        return redirect(session["url"])
    except:
        flash("Error deleting transaction", "error")
        return redirect(session["url"])


