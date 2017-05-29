import datetime
import logging
from connexion import NoContent
import connexion
from database import db
from database.models import Lockerbox, User
import uuid

log = logging.getLogger(__name__)

def list(lockersetcode=None, onlyavailable=False, onlyone=False):
    log.debug('list: lockersetcode: %s, onlyavailable: %s, onlyOne: %s' % (lockersetcode, onlyavailable, onlyone))
    token = connexion.request.headers['token']
    #--- TODO: check token
    lockerboxes = Lockerbox.query.filter(Lockerbox.lockerset_code == lockersetcode)
    if onlyavailable:
        log.debug('only available')
        lockerboxes = lockerboxes.filter(Lockerbox.status == Lockerbox.STATUS_EMPTY)
    if onlyone:
        log.debug('only one')
        lockerboxes = lockerboxes.first()
    return Lockerbox.serialize_list(lockerboxes)

def put(lockerboxcode=None, operation=None, user=None, key=None ):
    log.debug('put: lockerboxcode: %s, operation: %s, user: %s, key: %s' % (lockerboxcode, operation, user, key))
    token = connexion.request.headers['token']
    #--- TODO: check token

    lockerbox = Lockerbox.query.filter(Lockerbox.lockerbox_code == lockerboxcode).first()
    if lockerbox is None:
        return { 'msg': 'lockerbox not found' }, 400
    if operation == 'Assign':
        log.debug('operation: Assign')
        if user is None:
            return {'msg': 'User must be provided'}, 400
        userObj = User.query.filter(User.email == user).first()
        if userObj is None:
            return {'msg': 'User not found'}, 400
        log.debug('no errors')
        lockerbox.user = user
        lockerbox.status = Lockerbox.STATUS_ASSIGNED
        lockerbox.key = '123'
        db.session.commit()
        log.debug('lockerbox: %s' % lockerbox.serialize())
        return lockerbox.serialize(), 200
    
    return { 'msg': 'Invalid operation' }, 400