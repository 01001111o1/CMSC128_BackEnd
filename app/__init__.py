from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
#from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "testing.db"

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
app.config["FILE_UPLOADS"] = "C:/Users/Sean/Desktop/CMSC128Project/Testing"
app.config["ALLOWED_FILE_EXTENSIONS"] = ["PDF"]
app.config["MAX_FILE_FILESIZE"] = 0.5 * 1024 * 1024 * 1024
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

from .views import views
from .admin_views import admin_views

app.register_blueprint(views, url_prefix = '/')
app.register_blueprint(admin_views, url_prefix = '/')


from .models import Request

with app.app_context():
	db.create_all()






















