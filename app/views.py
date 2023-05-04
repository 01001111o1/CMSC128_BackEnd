from app import app
from app import Lists 
from flask import render_template, request, redirect, jsonify, make_response, url_for, session

import os
from werkzeug.utils import secure_filename

from email_validator import validate_email, EmailNotValidError


@app.route("/")
def index():
    return render_template("public/index.html")

#Requirement = [list of documents that require it]

@app.route("/choose_requirements", methods = ["GET", "POST"])
def choose_requirements():
    if request.method == "POST":

        YearLevel = request.form.get("YearLevel")

        email = request.form.get("email")

        try:

          emailinfo = validate_email(email, check_deliverability=True)
          email = emailinfo.normalized

        except EmailNotValidError as e:
          print(str(e)) #Turn it into a JS alert or something
          return redirect(request.url)

        documents = request.form.getlist("check") #Requested Documents
        if len(documents) == 0:
            #alert message to select at least one
            return redirect(request.url)

        for k, _ in Lists.Requirements.items():
            session[k] = any([val in documents for val in Lists.Requirements[k]])

        session.modified = True

        return redirect(url_for("upload_image"))

    return render_template("public/choose_requirements.html", list1 = Lists.Documents1 ,list2 = Lists.Documents2)

def index():
    return render_template("public/index.html")

app.config["FILE_UPLOADS"] = "C:/Users/Sean/Desktop/CMSC128Project/Testing"
app.config["ALLOWED_FILE_EXTENSIONS"] = ["PDF"]
app.config["MAX_FILE_FILESIZE"] = 0.5 * 1024 * 1024 * 1024

def allowed_file(filename):
    if not "." in filename:
        return False
    return filename.rsplit(".", 1)[1].upper() in app.config["ALLOWED_FILE_EXTENSIONS"]

def allowed_file_size(filesize):
    return int(filesize) <= app.config["MAX_FILE_FILESIZE"]

@app.route("/upload_image", methods = ["GET", "POST"])
def upload_image():

    if request.method == "POST":
        if request.files:

            name = request.form.get("name")
            files = request.files.getlist("file")
            for file in files:
                if not allowed_file_size(request.cookies.get("filesize")):
                    print("File exceeded maximum size")
                    return redirect(request.url)
                
                if file.filename == "":
                    print("File must have a filename")
                    return redirect(request.url)

                if not allowed_file(file.filename):
                    print("Invalid file extension")
                    return redirect(request.url)

            new_directory = app.config["FILE_UPLOADS"] + "/" + name
            os.mkdir(new_directory)
                
            for file in files:
                filename = secure_filename(file.filename)
                file.save(os.path.join(new_directory, filename))

            return redirect(request.url)

    return render_template("public/upload_image.html")






