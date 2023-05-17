from flask import render_template, request, redirect, jsonify, make_response, url_for, session, flash, Blueprint
from . import db
from app import app
from .models import Request
import shutil

admin_views = Blueprint('admin_views', __name__)


@admin_views.route("/admin/dashboard")
def admin_dashbard():
    requests = Request.query.all()

    return render_template("admin/dashboard.html", requests = requests)

@admin_views.route("/delete/<int:queue_number>")
def delete_entry(queue_number):
    query = Request.query.get_or_404(queue_number)  
    folder_name =" ".join([query.first_name.upper(), query.middle_name.upper(), query.last_name.upper()])
    folder_path = app.config["FILE_UPLOADS"] + "/" + folder_name

    try:
        shutil.rmtree(folder_path, ignore_errors = False)
    except:
        flash("error deleting folder", "error")
        return redirect(url_for("admin_views.admin_dashbard"))

    try:
        db.session.delete(query)
        db.session.commit()
        flash("Transaction successfully deleted", "success")
        return redirect(url_for("admin_views.admin_dashbard"))
    except:
        flash("Error deleting transaction", "error")
        return redirect(url_for("admin_views.admin_dashbard"))



