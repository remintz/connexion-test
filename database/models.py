# The examples in this file come from the Flask-SQLAlchemy documentation
# For more information take a look at:
# http://flask-sqlalchemy.pocoo.org/2.1/quickstart/#simple-relationships

from database import db
from sqlalchemy.inspection import inspect
import logging

log = logging.getLogger(__name__)

class Serializer(object):
    def serialize(self):
        return {c: getattr(self, c) for c in inspect(self).attrs.keys()}

    @staticmethod
    def serialize_list(l):
        return [m.serialize() for m in l]

class Lockerset(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50))
    numBoxes = db.Column(db.Integer)

    def __init__(self, code, numBoxes):
        self.code = code
        self.numBoxes = numBoxes

    def __repr__(self):
        return '<Lockerset %r>' % self.code

    def serialize(self):
        d = Serializer.serialize(self)
        return d

class Session(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(50))
    expiration = db.Column(db.DateTime)
    token = db.Column(db.String(50))

    def __init__(self, login, expiration, token):
        self.login = login
        self.expiration = expiration
        self.token = token

    def __repr__(self):
        return '<Session %r>' % self.login

    def serialize(self):
        d = Serializer.serialize(self)
        return d

class Lockerbox(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    lockerbox_code = db.Column(db.String(60))
    lockerset_code = db.Column(db.String(50))
    status = db.Column(db.Integer)
    key = db.Column(db.String(50))
    STATUS_EMPTY, STATUS_FULL = range(2)

    def __init__(self, lockerset_code, box_number):
        log.debug('Lockerbox: lockerset_code: %s, box_number: %d' % (lockerset_code, box_number))
        self.lockerbox_code = "%s/%d" % (lockerset_code, box_number)
        self.lockerset_code = lockerset_code
        self.status = Lockerbox.STATUS_EMPTY
        self.key = ''
    
    def __repr__(self):
        return '<Lockerbox %s>' % self.lockerbox_code

    def serialize(self):
        d = Serializer.serialize(self)
        return d

class User(db.Model, Serializer):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))

    def __init__(self, email):
        log.debug('User: email: %s' % email)
        self.email = email

    def __repr__(self):
        return '<User %s>' % self.email

    def serialize(self):
        d = Serializer.serialize(self)
        return d

