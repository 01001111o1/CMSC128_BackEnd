from . import db
import datetime
import pytz

class Request(db.Model):
	queue_number = db.Column(db.Integer, primary_key = True, autoincrement = True)
	last_name = db.Column(db.String(30), nullable = False)
	first_name = db.Column(db.String(30), nullable = False)
	middle_name = db.Column(db.String(30), nullable = False)
	email = db.Column(db.String(50), nullable = False)
	year_level = db.Column(db.String(20), nullable = False)
	requested_documents = db.Column(db.String(600), nullable = False)
	total_price = db.Column(db.Integer)
	date_of_request = db.Column(db.DateTime(timezone = True), default = datetime.datetime.now(pytz.timezone('Singapore')).replace(microsecond = 0))
	request_approved = db.Column(db.Boolean(), default = False)
	documents_approved = db.Column(db.Boolean(), default = False)
	paid = db.Column(db.Boolean(), default = False)
	request_available = db.Column(db.Boolean(), default = False)

