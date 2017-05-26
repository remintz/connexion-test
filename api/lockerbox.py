import datetime
import logging
from connexion import NoContent
import connexion
from database import db
from database.models import Lockerbox
import uuid

log = logging.getLogger(__name__)

def list(lockersetCode=None, onlyAvailable=False, onlyOne=False):
    log.debug('list: lockersetCode: %s, onlyAvailable: %s, onlyOne: %s' % (lockersetCode, onlyAvailable, onlyOne))
    token = connexion.request.headers['token']
    #--- TODO: check token
    lockerboxes = []
    if lockersetCode is None or len(lockersetCode) == 0:
        lockerboxes = Lockerbox.query.all()
    else:
        if onlyAvailable:
            lockerboxes = Lockerbox.query. \
                filter(Lockerbox.lockerset_code == lockersetCode). \
                filter(Lockerbox.status == Lockerbox.STATUS_EMPTY)
        if onlyOne:
            lockerboxes = lockerboxes.first()
    return Lockerbox.serialize_list(lockerboxes)

def put():
    pass
