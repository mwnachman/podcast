import os
from config import config

from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_app(config_name='default'):
	app = Flask(__name__)
	app.config.from_object(config[config_name])
	config[config_name].init_app(app)

	db.init_app(app)

	from podcast.views.app import bp
	app.register_blueprint(bp, url_prefix='')

	return app
