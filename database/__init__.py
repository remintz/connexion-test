from flask_sqlalchemy import SQLAlchemy
import logging

log = logging.getLogger('__name__')
db = SQLAlchemy()

def reset_database(app):
    log.debug('reset_database')
    print('>>>>>>>>>>> reset_database')
    with app.app_context():
        db.drop_all()
        db.create_all()
