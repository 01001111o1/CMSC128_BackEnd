from flask import render_template, Blueprint
from . import db
from .models import Request

admin_views = Blueprint('admin_views', __name__)


@admin_views.route("/admin/dashboard")
def admin_dashbard():
    requests = Request.query.all()

    return render_template("admin/dashboard.html", requests = requests)



