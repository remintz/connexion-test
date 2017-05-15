import logging.config
import connexion
from connexion.resolver import RestyResolver
from flask import Flask, Blueprint
import settings
from smartlocker_api.api.endpoints.lockersets import ns as lockersets_namespace
#from smartlocker_api.api.endpoints.users import ns as users_namespace
from smartlocker_api.api.restplus import api
from smartlocker_api.database import db, reset_database


app = connexion.FlaskApp(__name__, 9090, specification_dir='swagger/')
logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)

def configure_app(flask_app):
    flask_app.config['SERVER_NAME'] = settings.FLASK_SERVER_NAME
    flask_app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
    flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
    flask_app.config['SWAGGER_UI_DOC_EXPANSION'] = settings.RESTPLUS_SWAGGER_UI_DOC_EXPANSION
    flask_app.config['RESTPLUS_VALIDATE'] = settings.RESTPLUS_VALIDATE
    flask_app.config['RESTPLUS_MASK_SWAGGER'] = settings.RESTPLUS_MASK_SWAGGER
    flask_app.config['ERROR_404_HELP'] = settings.RESTPLUS_ERROR_404_HELP



def initialize_app(flask_app):
    configure_app(flask_app)

#    blueprint = Blueprint('api', __name__, url_prefix='/api')
#    api.init_app(blueprint)
#    api.add_namespace(lockersets_namespace)
#    flask_app.register_blueprint(blueprint)
    db.init_app(flask_app)
    if settings.RESET_DATABASE:
        reset_database(flask_app)


def main():
    flask_app = app.app
    initialize_app(flask_app)
    log.info('>>>>> Starting development server at http://{}/ <<<<<'.format(flask_app.config['SERVER_NAME']))
    app.add_api('smartlocker_api.yaml', resolver=RestyResolver('api'))
    app.run(debug=settings.FLASK_DEBUG)

if __name__ == "__main__":
    main()
