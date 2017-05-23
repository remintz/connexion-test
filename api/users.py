import datetime
import logging
from connexion import NoContent

log = logging.getLogger(__name__)
users = {}

def get(id):
    id = int(id)
    if users.get(id) is None:
        return NoContent, 404
    return users[id]

def search():
    return list(users.values())

def post(user):
    print('users.post')
    log.debug('POST')
    count = len(users)
    user['id'] = count + 1
    user['created'] = datetime.datetime.now()
    users[user['id']] = user
    return user, 201

def delete(id):
    id = int(id)
    if users.get(id) is None:
        return NoContent, 404
    del users[id]
    return NoContent, 204