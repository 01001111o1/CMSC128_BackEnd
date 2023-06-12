from . import db
from datetime import datetime
import pytz

from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_login import UserMixin 

from app import login

class Request(db.Model):
	queue_number = db.Column(db.Integer, primary_key = True, autoincrement = True)
	last_name = db.Column(db.String(30), nullable = False)
	first_name = db.Column(db.String(30), nullable = False)
	middle_name = db.Column(db.String(30), nullable = False)
	email = db.Column(db.String(50), unique = True, nullable = False)
	student_number = db.Column(db.String(10), unique = True, nullable = False)
	year_level = db.Column(db.String(20), nullable = False)
	requested_documents = db.Column(db.String(600), nullable = False)
	remarks = db.Column(db.String(150), nullable = False)
	price_map = db.Column(db.String(800), nullable = False)
	total_price = db.Column(db.Integer)
	date_of_request = db.Column(db.DateTime(timezone = True), default = datetime.now(pytz.timezone('Singapore')).replace(microsecond = 0))
	payment_date = db.Column(db.DateTime(timezone = True), default = None)
	request_paid = db.Column(db.Boolean(), default = False)
	request_approved = db.Column(db.Boolean(), default = False)
	documents_approved = db.Column(db.Boolean(), default = False)
	request_available = db.Column(db.Boolean(), default = False)

@login.user_loader
def load_user(id):
    return Admin.query.get(int(id))

class Admin(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key = True, autoincrement = True)
	username = db.Column(db.String(30), unique = True, nullable = False)
	email = db.Column(db.String(50), unique = True, nullable = False)
	password = db.Column(db.String(150), nullable = False)





