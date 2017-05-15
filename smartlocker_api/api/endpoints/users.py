import logging

from flask import request
from flask_restplus import Resource, fields
from smartlocker_api.api.business import create_lockerset, delete_lockerset#, update_lockerset
#from smartlocker_api.api.serializers import lockerset
from smartlocker_api.api.restplus import api
from smartlocker_api.database.models import Lockerset
from smartlocker_api.util import ValidationError

log = logging.getLogger(__name__)

ns = api.namespace('users', description='Operations related to users')

userModel = api.model('User', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a user'),
    'email': fields.String(required=True, description='User e-mail')
})

@ns.route('/')
class UsersCollection(Resource):

    @api.marshal_list_with(userModel)
    def get(self):
        """
        Returns list of users.
        """
        users = User.query.all()
        return users

    @api.response(201, 'User successfully created.')
    @api.response(409, 'User already exists')
    @api.expect(userModel)
    @api.marshal_list_with(userModel)
    def post(self):
        """
        Creates a new user.
        """
        data = request.json
        user = create_user(data) 
        return user, 201


@ns.route('/<int:id>')
@api.response(404, 'User not found.')
class LockersetItem(Resource):

    @api.marshal_list_with(userModel)
    def get(self, id):
        """
        Returns a user.
        """
        return User.query.filter(User.id == id).one()

    @api.response(204, 'User successfully deleted.')
    def delete(self, id):
        """
        Deletes a user.
        """
        delete_user(id)
        return None, 204
