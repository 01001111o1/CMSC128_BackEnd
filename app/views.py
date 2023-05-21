from app import app
from .Lists import Documents1, Documents2, Requirements, Base_Prices, scholarship_discounted_documents
from flask import render_template, request, redirect, jsonify, make_response, url_for, session, flash, Blueprint, escape

import os
import io 
from werkzeug.utils import secure_filename

from email_validator import validate_email, EmailNotValidError

from . import db
from .models import Request

views = Blueprint('views', __name__)

@views.route("/")
def index():
    return render_template("public/index.html")


def isInvalid(name):
    invalid_symbols = ['<', '>', '"', '&']
    for symbol in invalid_symbols:
        if name.find(symbol) != -1:
            return True
    return False

@views.route("/choose_requirements", methods = ["GET", "POST"])
def choose_requirements():
    if request.method == "POST":

        name = request.form.getlist("name")

        for n in name:
            if isInvalid(n):
                flash("Invalid characters in input form", "error")
                return redirect(request.url)

        email = request.form.get("email")
        student_number = request.form.get("student_number")
        total_price = request.form.get("total_price")
        year_level = request.form.get("YearLevel")
        documents = request.form.getlist("check")

        price_map = request.form.get("map")

        if len(student_number) != 9:
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

    return render_template("public/choose_requirements.html", list1 = Documents1, list2 = Documents2, scholarship_documents = 
        scholarship_discounted_documents, base_prices = Base_Prices)

def allowed_file(filename):
    if not "." in filename:
        return False
    return filename.rsplit(".", 1)[1].upper() in app.config["ALLOWED_FILE_EXTENSIONS"]

def allowed_file_size(filesize):
    return int(filesize) <= app.config["MAX_FILE_FILESIZE"]

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

                folder_name = " ".join([name.upper() for name in session["name"]])

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
                    price_map = session["price_map"],
                    total_price = session["total_price"]
                )

            db.session.add(new_request)
            db.session.commit()

            session.clear()

            flash("Successfully posted a request", "success")
            return redirect(url_for("views.index"))

    return render_template("public/upload_image.html")






