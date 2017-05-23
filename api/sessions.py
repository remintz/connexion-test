import datetime
import logging
from connexion import NoContent

log = logging.getLogger(__name__)
sessions = {}

def post(session):
    print('session.post')
    log.debug('POST')
    count = len(sessions)
    session['id'] = count + 1
    session['created'] = datetime.datetime.now()
    sessions[session['id']] = session
    return session, 201

