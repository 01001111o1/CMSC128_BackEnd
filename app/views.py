from app import app
from .Lists import Documents1, Documents2, Requirements, Base_Prices, scholarship_discounted_documents, YearLevel_Map
from flask import render_template, request, redirect, jsonify, make_response, url_for, session, flash, Blueprint, escape

import os
import io 
from werkzeug.utils import secure_filename

from email_validator import validate_email, EmailNotValidError

from . import db
from .models import Request, Admin

from flask_login import current_user

from .functions import allowed_file, allowed_file_size, isInvalid

from werkzeug.security import generate_password_hash, check_password_hash

from .send_generated_files import background_runner

views = Blueprint('views', __name__)

@views.route("/")
@views.route("/home")
def index():
    return render_template("public/intro.html", user = current_user)

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
            int(student_number)
        except:
            flash("Please enter a valid student number", "error")
            return redirect(request.url)

        try:

          emailinfo = validate_email(email, check_deliverability=True)
          email = emailinfo.normalized

        except:
          flash("Enter a valid email", "error")
          return redirect(request.url)

        if len(documents) == 0:
            flash("Select at least one requirement", "error")
            return redirect(request.url)

        temp = dict()

        for k, _ in Requirements.items():
            temp[k] = any([val in documents for val in Requirements[k]])

        session["remarks"] = [purpose]

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
        session.modified = True

        return redirect(url_for("views.upload_image"))

    return render_template("public/request_forms.html", list1 = Documents1, list2 = Documents2, scholarship_documents = 
        scholarship_discounted_documents, base_prices = Base_Prices, user = current_user)

@views.route("/upload_image", methods = ["GET", "POST"])
def upload_image():

    if request.method == "POST":
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

            if "True Copy of Grades" in session["documents"]:
                session["remarks"].append("Preferred TCG Format: " + request.form.get("preferred_format"))

            folder_name = " ".join([name.upper() for name in session["name"]])

            check_email = Request.query.filter_by(email = session["email"]).first()
            check_student_number = Request.query.filter_by(student_number = session["student_number"]).first()

            if check_email:
                flash("Email already exists", "error") #pag bawal 2 request kada student
                return redirect(url_for("views.request_forms"))

            if check_student_number:
                flash("Student number already exists", "error") #pag bawal 2 request kada student
                return redirect(url_for("views.request_forms"))

            new_directory = app.config["FILE_UPLOADS"] + "/" + folder_name
            os.mkdir(new_directory)
                
            for file in files:
                filename = secure_filename(file.filename)
                file.save(os.path.join(new_directory, filename))

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

            session.clear()

            latest_request = Request.query.order_by(Request.queue_number.desc()).first()
            background_runner.send_email_async(latest_request.queue_number)

            flash("Successfully posted a request", "success")
            return redirect(url_for("views.index"))

    return render_template("public/upload_image.html", user = current_user)






