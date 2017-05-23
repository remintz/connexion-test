import datetime
import logging
from connexion import NoContent

log = logging.getLogger(__name__)
lockersets = {}

def post(lockerset):
    log.debug('POST')
    count = len(lockersets)
    lockerset['id'] = count + 1
    lockerset['created'] = datetime.datetime.now()
    lockersets[lockerset['id']] = lockerset
    return lockerset, 201

def search():
    return list(lockersets.values())

def delete(id):
    id = int(id)
    if lockersets.get(id) is None:
        return NoContent, 404
    del lockersets[id]
    return NoContent, 204

def get(id):
    id = int(id)
    if lockersets.get(id) is None:
        return NoContent, 404
    return lockersets[id]

def put(id, lockerset):
    id = int(id)
    if lockersets.get(id) is None:
        return NoContent, 404
    lockersets[id] = lockerset
    return lockersets[id]
    