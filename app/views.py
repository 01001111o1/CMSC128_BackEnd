from app import Lists, app
from flask import render_template, request, redirect, jsonify, make_response, url_for, session, flash, Blueprint, escape

# import drive_demo as drive
# from drive_demo import search_folder
# from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload

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

@views.route("/choose_requirements", methods = ["GET", "POST"])
def choose_requirements():
    if request.method == "POST":

        name = request.form.getlist("name")
        name = [escape(n) for n in name]
        email = escape(request.form.get("email"))
        total_price = escape(request.form.get("total_price"))
        year_level = escape(request.form.get("YearLevel"))
        documents = request.form.getlist("check")

        try:

          emailinfo = validate_email(email, check_deliverability=True)
          email = emailinfo.normalized

        except EmailNotValidError as e:
          flash("Enter a valid email", "error")
          return redirect(request.url)

        if len(documents) == 0:
            flash("Select at least one requirement", "error")
            return redirect(request.url)

        temp = dict()

        for k, _ in Lists.Requirements.items():
            temp[k] = any([val in documents for val in Lists.Requirements[k]])

        session["requirements"] = temp

        session["name"] = name
        session["email"] = email
        session["total_price"] = total_price
        session["year_level"] = year_level
        session["documents"] = "@".join(documents)
        session.modified = True


        return redirect(url_for("views.upload_image"))

    return render_template("public/choose_requirements.html", list1 = Lists.Documents1, list2 = Lists.Documents2, scholarship_documents = 
        Lists.scholarship_discounted_documents, base_prices = Lists.Base_Prices)

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

                # file_metadata = {
                #     'name' : folder_name,
                #     'mimeType' : 'application/vnd.google-apps.folder'  
                # }

                # drive.service.files().create(body = file_metadata).execute()
                # folder_id = search_folder(folder_name)

                # for file in files:
                #     file_metadata = {
                #         'name' : secure_filename(file.filename),
                #         'parents' : [folder_id]
                #     }

                #     buffer = io.BytesIO()
                #     buffer.name = file.filename
                #     file.save(buffer)
                #     media = MediaIoBaseUpload(buffer, mimetype='application/pdf', resumable=True)

                #     drive.service.files().create(
                #         body = file_metadata,
                #         media_body = media,
                #         fields = 'id'
                #     ).execute()
                #IF CANT FIX MULTIPLE FOLDERS, NEED TO MAKE FILE TYPE ZIP

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
                    year_level = session["year_level"],
                    requested_documents = session["documents"],
                    total_price = session["total_price"]
                )

            db.session.add(new_request)
            db.session.commit()

            session.clear()

            flash("Successfully posted a request", "success")
            return redirect(url_for("views.index"))

    return render_template("public/upload_image.html")






