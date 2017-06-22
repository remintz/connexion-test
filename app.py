#!/usr/bin/env python3
import connexion
import datetime
import logging
import settings
import os

from connexion import NoContent
from database import db, reset_database

def init_db(application, reset_db):
    db.init_app(application)
    if reset_db:
        reset_database(application)

def configure_app(flask_app):
    flask_app.config['SERVER_PORT'] = settings.FLASK_SERVER_PORT
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP
    flask_app.config['DEBUG'] = settings.FLASK_DEBUG

logging.basicConfig(level=logging.INFO)
app = connexion.FlaskApp("smartlocker_api", server='tornado')
flask_app = app.app
application = app.app # expose global WSGI application object

app.add_api('swagger.yaml')
configure_app(flask_app)
init_db(flask_app, settings.RESET_DATABASE)

if __name__ == '__main__':
    # run our standalone gevent server
    web_port = int(os.environ.get('PORT', settings.FLASK_SERVER_PORT))
    app.run(port=web_port)
