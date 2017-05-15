# The examples in this file come from the Flask-SQLAlchemy documentation
# For more information take a look at:
# http://flask-sqlalchemy.pocoo.org/2.1/quickstart/#simple-relationships

from smartlocker_api.database import db

class Lockerset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50))
    numBoxes = db.Column(db.Integer)

    def __init__(self, code, numBoxes):
        self.code = code
        self.numBoxes = numBoxes

    def __repr__(self):
        return '<Lockerset %r>' % self.code

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))

    def __init__(self, email):
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.emails

