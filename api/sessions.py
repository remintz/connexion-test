import datetime
import connexion

def create():
    email = connexion.request.headers['email']
    password = connexion.request.headers['password']
    result = '{ "login": %s, "pwd": %s }' % (email, password)
    return result, 201

