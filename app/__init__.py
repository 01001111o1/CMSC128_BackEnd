from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from flask_login import LoginManager
from flask_executor import Executor
from apscheduler.schedulers.blocking import BlockingScheduler

db = SQLAlchemy()
DB_NAME = "testing.db"
dirname = os.path.dirname(os.path.abspath(__file__))
filename = dirname.replace('\\','/')

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.config['SECRET_KEY'] = '8DMC9QP_ppb_7-spe_tppDB07zSaABvDIRHjbvUvgtkAj_JQqSy3UsC2l00o4VWMGsiJPujsxYn06ZJS9HnQuQ'
app.config["FILE_UPLOADS"] = filename.replace('app','Requirements')
app.config["PAYMENT_UPLOADS"] = filename.replace('app','Payments')
app.config["ALLOWED_FILE_EXTENSIONS"] = ["PDF"]
app.config["MAX_FILE_FILESIZE"] = 32 * 1000 * 1000
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['REQUESTS_PER_PAGE'] = 5
app.config['QR_CODE_PATH'] = filename + '/static/imgs/icons/qr-code-payment-form.png'
db.init_app(app)

executor = Executor(app)

login = LoginManager()
login.login_view = 'auth.login'
login.init_app(app)

scheduler = BlockingScheduler()

from .views import views
from .admin_views import admin_views
from .auth import auth

app.register_blueprint(views, url_prefix = '/')
app.register_blueprint(admin_views, url_prefix = '/')
app.register_blueprint(auth, url_prefix = '/')

with app.app_context():
	db.create_all()





















