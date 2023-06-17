"""

File contains the routes that are accessible from the user (non-admin side)

2023 UPB2GO

"""

from app import app
from .Lists import Documents1, Documents2, Requirements, Base_Prices, scholarship_discounted_documents, YearLevel_Map
from flask import render_template, request, redirect, jsonify, make_response, url_for, session, flash, Blueprint, escape
import os
import os.path
import io 
from werkzeug.utils import secure_filename
from email_validator import validate_email, EmailNotValidError
from . import db
from .models import Request, Admin
from flask_login import current_user
from .functions import allowed_file, allowed_file_size, isInvalid
from .background_runner import background_runner

views = Blueprint('views', __name__)

"""
Route that displays the home page

"""
@views.route("/")
@views.route("/home")
def index():
    return render_template("public/intro.html", user = current_user)

"""

Route that displays the page for requesting forms

Relevant requester information is pulled from their form response and stored in a session variable.

Additional backend form validation is done such as checking for invalid characters in the form input to prevent SQLI attacks and checking for
email deliverability

If the number of documents that needs to be submitted is 0 then it implies that it would have only needed proof of payment for it to start
being processed. As such, the page for uploading requirements is skipped entirely and a new request is inserted into the database

"""
@views.route("/request_forms", methods = ["GET", "POST"])
def request_forms():
    if request.method == "POST":

        name = [name.upper() for name in request.form.getlist("name")]
        email = request.form.get("email")
        student_number = request.form.get("student_number")
        total_price = request.form.get("total_price")
        year_level = YearLevel_Map[request.form.get("YearLevel")]
        documents = request.form.getlist("check")
        scholarship = request.form.get("scholarship")
        purpose = "Purpose: " + request.form.get("purpose").upper()
        price_map = request.form.get("map")
        mode_of_payment = request.form.get("payment_method")

        temp = dict()
        count = 0

        for k, _ in Requirements.items():
            temp[k] = any([val in documents for val in Requirements[k]])
            count += 1 if temp[k] == True else 0

        for n in name:
            if isInvalid(n):
                flash("Invalid characters in input form", "error")
                return redirect(request.url)
        
        if isInvalid(purpose):
            flash("Please enter valid characters in input form", "error")
            return redirect(request.url)

        if len(student_number) != 9 or not student_number.isdigit() or student_number[0:2] != "20":
            flash("Please enter a valid student number", "error")
            return redirect(request.url)   

        try:

          emailinfo = validate_email(email, check_deliverability = True)
          email = emailinfo.normalized

        except:
          flash("Enter a valid email", "error")
          return redirect(request.url)

        if len(documents) == 0:
            flash("Select at least one requirement", "error")
            return redirect(request.url)

        session["remarks"] = [purpose]
        session["remarks"].append("Mode of payment: " + mode_of_payment)

        if scholarship is not None:
            session["remarks"].append("For Scholarship")

        session["requirements"] = temp
        session["name"] = name
        session["email"] = email
        session["student_number"] = student_number[:4] + '-' + student_number[4:]
        session["total_price"] = total_price
        session["year_level"] = year_level
        session["documents"] = "@".join(documents)
        session["price_map"] = price_map
        session["count"] = count
        session.modified = True

        if count == 0:
            new_request()
            flash("Successfully posted a request", "success")
            return redirect(url_for("views.index"))

        return redirect(url_for("views.upload_image"))

    return render_template("public/request_forms.html", list1 = Documents1, list2 = Documents2, scholarship_documents = 
        scholarship_discounted_documents, base_prices = Base_Prices, user = current_user)

"""

Routes that display pages for the about page, contact page, and the FAQs respectively

"""
@views.route("/about_us")
def about_us():
    return render_template("public/about-us.html", user = current_user)

@views.route("/contact_us")
def contact_us():
    return render_template("public/contact-us.html", user = current_user)

@views.route("/faqs")
def faqs():
    return render_template("public/faqs.html", user = current_user)

"""
new_request: function

Function that processes a new request based on the current user's session variable contents. 
It first checks for duplicate entries by email, or student number. 

First creates a folder in the local server based on the requester's full name then inserts the request in the database
After doing so, the request number is pulled from the database with which a function to asynchronously send an email is performed to send
the invoice of the requester's requested documents.

To follow: implementation for duplicate requests where we may opt to merge the requested documents and update the price if so

"""

def new_request():

    check_email = Request.query.filter_by(email = session["email"]).first()
    check_student_number = Request.query.filter_by(student_number = session["student_number"]).first()

    if "True Copy of Grades" in session["documents"]:
        session["remarks"].append("Preferred TCG Format: " + request.form.get("preferred_format"))

    if check_email or check_student_number:
        flash("You currently have a request in progress") #Maybe handle duplicate entries
        return redirect(url_for("views.request_forms"))

    folder_name = " ".join([name.upper() for name in session["name"]])

    new_directory = app.config["FILE_UPLOADS"] + "/" + folder_name
    session["path"] = str(new_directory)

    if not os.path.isdir(new_directory):
        os.mkdir(new_directory)

    new_request = Request(
            last_name = session["name"][2],
            first_name = session["name"][0],
            middle_name = session["name"][1],
            email = session["email"],
            student_number = session["student_number"],
            year_level = session["year_level"],
            requested_documents = session["documents"],
            remarks = "@".join(session["remarks"]),
            price_map = session["price_map"],
            total_price = session["total_price"]
        )

    db.session.add(new_request)
    db.session.commit()

    latest_request = Request.query.order_by(Request.queue_number.desc()).first()
    background_runner.send_invoice_or_receipt_asynch(latest_request.queue_number, "invoice")
    session.clear()

"""
Route to display the page for uploading requirements.

In the case where documents other than the proof of payment is required for processing a request, the user is redirected to this page 
where one can upload each pdf requirement associated with his requested documents.

File verification includes:
    checking if every file is within the file size limit (32 mb)
    checking if every file name has a name
    checking for file extensions (only PDFs are allowed)

After verifying that the uploaded documents are valid, a new request is inserted and the associated files are downloaded into a folder
in the server with a folder name corresponding to the name of the requester.

"""
@views.route("/upload_image", methods = ["GET", "POST"])
def upload_image():

    if request.method == "POST":

        if "True Copy of Grades" in session["documents"] and session["count"] == 1:
            new_request()
            return redirect(url_for("views.index"))

        if request.files:

            files = request.files.getlist("file")

            for file in files:
                if not allowed_file_size(request.cookies.get("filesize")):
                    flash("File size too large", "error")
                    return redirect(request.url)
                
                if file.filename == "":
                    flash("File must have a name", "error")
                    return redirect(request.url)

                if not allowed_file(file.filename):
                    flash("Invalid file extension", "error")
                    return redirect(request.url)

            new_request()

            for file in files:
                filename = secure_filename(file.filename)
                file.save(os.path.join(session["path"], filename))

            flash("Successfully posted a request", "success")
            return redirect(url_for("views.index"))

    return render_template("public/upload_image.html", user = current_user)






