import datetime
import logging
from connexion import NoContent
import connexion
from database import db
from database.models import Lockerset, Lockerbox
import uuid

log = logging.getLogger(__name__)

def create():
    token = connexion.request.headers['token']
    #--- TODO: check token
    code = connexion.request.headers['code'].upper()
    numBoxes = int(connexion.request.headers['numBoxes'])
    log.debug("POST code: %s, numBoxes: %s" % (code, numBoxes))
    lockerset = Lockerset.query.filter(Lockerset.code == code).first()
    if lockerset is not None:
        log.debug('lockerset already exists')
        return NoContent, 409
    if numBoxes < 1:
        log.debug('numboxes out of range')
        return NoContent, 400
    lockerset = Lockerset(code, numBoxes)
    db.session.add(lockerset)
    #--- add lockerboxes for this lockerset
    log.debug('creating %d boxes' % numBoxes)
    for box in range(1, numBoxes+1):
        lockerbox = Lockerbox(code, box)
        db.session.add(lockerbox)
    db.session.commit()
    log.debug('lockerset created')
    return lockerset.serialize(), 201

def list():
    token = connexion.request.headers['token']
    #--- TODO: check token
    lockersets = Lockerset.query.all()
    return Lockerset.serialize_list(lockersets)

def delete(lockerset_code):
    token = connexion.request.headers['token']
    #--- TODO: check token
    lockerset = Lockerset.query.filter(Lockerset.code == lockerset_code).first()
    if lockerset is not None:
        db.session.delete(lockerset)
        db.session.commit()
    return NoContent, 204

def get(lockerset_code):
    token = connexion.request.headers['token']
    #--- TODO: check token
    lockerset = Lockerset.query.filter(Lockerset.code == lockerset_code).first()
    if lockerset is None:
        return NoContent, 204
    return lockerset.serialize(), 201
