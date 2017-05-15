import logging
import traceback
from flask import jsonify
from flask_restplus import Api
from smartlocker_api import settings
from sqlalchemy.orm.exc import NoResultFound
from smartlocker_api.util import ValidationError

log = logging.getLogger(__name__)
api = Api(version='1.0', title='SmartLocker API',
          description='SmartLocker API')

@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)

    if not settings.FLASK_DEBUG:
        return {'message': message}, 500

@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    print('database_not_found_error_handler')
    log.warning(traceback.format_exc())
    return {'message': 'A database result was required but none was found.'}, 404

@api.errorhandler(ValidationError)
def handle_validation_error(error):
    log.warning(traceback.format_exc())
    return {'message': error.message }, error.status_code
