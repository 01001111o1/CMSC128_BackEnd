from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
app.config["FILE_UPLOADS"] = "C:/Users/Sean/Desktop/CMSC128Project/Testing"
app.config["ALLOWED_FILE_EXTENSIONS"] = ["PDF"]
app.config["MAX_FILE_FILESIZE"] = 0.5 * 1024 * 1024 * 1024
#app.config.from_object("config.DevelopmentConfig")

from app import views
from app import admin_views

























