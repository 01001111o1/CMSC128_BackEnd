from flask import render_template, request, redirect, jsonify, make_response, url_for, session, flash, Blueprint
from . import db
from app import app, Lists
from .models import Request
import shutil

from send_email import send_message

admin_views = Blueprint('admin_views', __name__)


@admin_views.route("/admin/dashboard")
def admin_dashboard():
    requests = Request.query.all()

    return render_template("admin/dashboard.html", requests = requests)

@admin_views.route("/update/<int:queue_number>/<classification>")
def update(queue_number, classification):
    query = Request.query.get_or_404(queue_number)  
    try:
        if classification == "request_approved":
            send_message("scvizconde@up.edu.ph", 
                query.email, 
                f"Request approved for order number { query.queue_number }", 
                "Test \n Content \n hehe") #MODIFY THE CONTENT, CREATE A TEMPLATE MESSAGE IN LISTS.PY
        elif classification == "documents_approved":
            send_message("scvizconde@up.edu.ph", 
                query.email, 
                f"Documents approved for order number { query.queue_number }", 
                "Test \n Content \n hehe")
        elif classification == "payment_received":
            send_message("scvizconde@up.edu.ph", 
                query.email, 
                f"Payment received for order number { query.queue_number }", 
                "Test \n Content \n hehe")
        else:
            send_message("scvizconde@up.edu.ph", 
                query.email, 
                f"order number { query.queue_number } available for claiming", 
                "Test \n Content \n hehe")
        flash("Successfully sent update email", "success")
        return redirect(url_for("admin_views.admin_dashboard"))
    except:
        flash("error sending update email", "error")
        return redirect(url_for("admin_views.admin_dashboard"))

@admin_views.route("/delete/<int:queue_number>")
def delete_entry(queue_number):
    query = Request.query.get_or_404(queue_number)  
    folder_name =" ".join([query.first_name.upper(), query.middle_name.upper(), query.last_name.upper()])
    folder_path = app.config["FILE_UPLOADS"] + "/" + folder_name

    try:
        shutil.rmtree(folder_path, ignore_errors = False)
    except:
        flash("error deleting folder", "error")
        return redirect(url_for("admin_views.admin_dashboard"))

    try:
        db.session.delete(query)
        db.session.commit()
        flash("Transaction successfully deleted", "success")
        return redirect(url_for("admin_views.admin_dashboard"))
    except:
        flash("Error deleting transaction", "error")
        return redirect(url_for("admin_views.admin_dashboard"))



