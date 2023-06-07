from app import app
from flask import render_template, request, redirect, Blueprint, flash, url_for
from flask_login import login_user, login_required, logout_user, current_user

from . import db
from .models import Request, Admin
from .functions import isInvalid
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint('auth', __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():

	if request.method == 'POST':

		email = request.form.get("email_login")
		password = request.form.get("password")
		admin = Admin.query.filter_by(email = email).first()

		if isInvalid(email) or isInvalid(password):
			flash("Invalid username or password", "error")
			return redirect(request.url)

		if not admin:
			flash("Email does not exist", "error")
			return redirect(request.url)
		if not check_password_hash(admin.password, password):
			flash("Password is incorrect", "error")
			return redirect(request.url)	

		login_user(admin, remember = True)
		flash("Logged in successfully", "success")
		return redirect(url_for("admin_views.admin_dashboard", parameter="default"))

	return render_template("public/login.html", user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.index'))



