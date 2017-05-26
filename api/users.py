import datetime
import logging
from connexion import NoContent
import connexion
from database import db
from database.models import User
import uuid

log = logging.getLogger(__name__)

def create():
    token = connexion.request.headers['token']
    #--- TODO: check token
    email = connexion.request.headers['email']
    user = User.query.filter(User.email == email).first()
    if user is not None:
        log.debug('user already exists')
        return NoContent, 409
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
    return NoContent, 204

def get(email):
    token = connexion.request.headers['token']
    #--- TODO: check token
    user = User.query.filter(User.email == email).first()
    if user is None:
        return NoContent, 204
    return user.serialize(), 201
