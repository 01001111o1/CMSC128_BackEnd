from flask import render_template, Blueprint

admin_views = Blueprint('admin_views', __name__)


@admin_views.route("/admin/dashboard")
def admin_dashbard():
    return render_template("admin/dashboard.html")

@admin_views.route("/admin/profile")
def admin_dashboard():
    return "Admin Profile"



