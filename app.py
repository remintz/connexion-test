#!/usr/bin/env python3
import connexion
import datetime
import logging
import settings
import os

from connexion import NoContent

def configure_app(flask_app):
    flask_app.config['SERVER_PORT'] = settings.FLASK_SERVER_PORT
    # flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP
    flask_app.config['DEBUG'] = settings.FLASK_DEBUG

logging.basicConfig(level=logging.INFO)
app = connexion.FlaskApp("smartlocker_api")
flask_app = app.app

app.add_api('swagger.yaml')
configure_app(flask_app)

if __name__ == '__main__':
    # run our standalone gevent server
    web_port = int(os.environ.get('PORT', settings.FLASK_SERVER_PORT))
    app.run(port=web_port, host='0.0.0.0')
