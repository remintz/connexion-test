import datetime
import logging
from connexion import NoContent
import connexion
from database import db
from database.models import Session
import uuid

log = logging.getLogger(__name__)

def create():
    email = connexion.request.headers['email']
    password = connexion.request.headers['password']
    log.debug('POST email: %s, password: %s' % (email, password))
    #--- find if session exists for this email
    session = Session.query.filter(Session.login == email).first()
    if session is not None:
        log.debug('session already exists')
        #--- check if expired
        now = datetime.datetime.now()
        if now < session.expiration:
            #--- session did not expired
            log.debug('session did not expire')
            return session.serialize(), 201
        else:
            #--- delete expired session
            log.debug('session expired')
            db.session.delete(session)
            db.session.commit()
    #--- there is no existing session or existing has expired, create one
    #--- TODO: check password
    expiration = datetime.datetime.now() + datetime.timedelta(seconds=60)
    token = str(uuid.uuid4())
    session = Session(email, expiration, token)
    db.session.add(session)
    db.session.commit()
    log.debug('session created: ')
    print(session.serialize())
    return session.serialize(), 201

