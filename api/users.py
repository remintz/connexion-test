import datetime
import logging
from connexion import NoContent
import connexion
from database import db
from database.models import User
import uuid
from api.return_status import get_ret_status

log = logging.getLogger(__name__)

def create():
    token = connexion.request.headers['token']
    #--- TODO: check token
    email = connexion.request.headers['email']
    user = User.query.filter(User.email == email).first()
    if user is not None:
        log.debug('user already exists')
        return get_ret_status('DUP_USER'), 409
    user = User(email)
    db.session.add(user)
    db.session.commit()
    log.debug('user created')
    return user.serialize(), 201

def list():
    token = connexion.request.headers['token']
    #--- TODO: check token
    users = User.query.all()
    return User.serialize_list(users)

def delete(email):
    token = connexion.request.headers['token']
    #--- TODO: check token
    user = User.query.filter(User.email == email).first()
    if user is not None:
        db.session.delete(user)
        db.session.commit()
    return get_ret_status('USER_DELETED'), 204

def get(email):
    token = connexion.request.headers['token']
    #--- TODO: check token
    user = User.query.filter(User.email == email).first()
    if user is None:
        return get_ret_status('USER_NOT_FOUND'), 404
    return user.serialize(), 201
