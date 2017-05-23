import datetime
import logging
from connexion import NoContent

log = logging.getLogger(__name__)
lockerboxes = {}

def get(id):
    id = int(id)
    if lockerboxes.get(id) is None:
        return NoContent, 404
    return lockerboxes[id]

def search():
    return list(lockerboxes.values())

def post(lockerbox):
    print('lockerboxes.post')
    log.debug('POST')
    count = len(lockerboxes)
    lockerbox['id'] = count + 1
    lockerbox['created'] = datetime.datetime.now()
    lockerboxes[lockerbox['id']] = lockerbox
    return lockerbox, 201

def delete(id):
    id = int(id)
    if lockerboxes.get(id) is None:
        return NoContent, 404
    del lockerboxes[id]
    return NoContent, 204

def put(id, lockerbox):
    id = int(id)
    if lockerboxes.get(id) is None:
        return NoContent, 404
    lockerboxes[id] = lockerbox
    return lockerboxes[id]