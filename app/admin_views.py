from app import app
from flask import render_template

@app.route("/admin/dashboard")
def admin_dashbard():
    return render_template("admin/dashboard.html")

@app.route("/admin/profile")
def admin_dashboard():
    return "Admin Profile"



