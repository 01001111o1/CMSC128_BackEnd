from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'

#app.config.from_object("config.DevelopmentConfig")

from app import views
from app import admin_views

























