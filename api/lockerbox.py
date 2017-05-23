import datetime
import logging
from connexion import NoContent
import connexion
from database import db
from database.models import Lockerbox
import uuid

log = logging.getLogger(__name__)

def list(lockersetCode, onlyAvailable=False, onlyOne=False):
    token = connexion.request.headers['token']
    #--- TODO: check token
    lockerboxes = Lockerbox.query.all()
    return Lockerbox.serialize_list(lockerboxes)

def put():
    pass
