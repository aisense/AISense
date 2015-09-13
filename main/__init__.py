from flask import Flask

__author__ = 'Gangeshwar'
application = Flask(__name__)

# application.config.from_object('config')

from main import views, models
