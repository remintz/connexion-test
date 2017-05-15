import logging

from flask import request
from flask_restplus import Resource, fields
from smartlocker_api.api.business import create_lockerset, delete_lockerset#, update_lockerset
#from smartlocker_api.api.serializers import lockerset
from smartlocker_api.api.restplus import api
from smartlocker_api.database.models import Lockerset
from smartlocker_api.util import ValidationError

log = logging.getLogger(__name__)

ns = api.namespace('lockersets', description='Operations related to lockersets')

lockerset = api.model('Lockerset', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a lockerset'),
    'code': fields.String(required=True, description='Lockerset code'),
    'numBoxes': fields.Integer(required=True, description='Number of boxes of a lockerset')
})

@ns.route('/')
class LockersetCollection(Resource):

    @api.marshal_list_with(lockerset)
    def get(self):
        """
        Returns list of lockersets.
        """
        lockersets = Lockerset.query.all()
        return lockersets

    @api.response(201, 'Lockerset successfully created.')
    @api.response(409, 'Lockerset already exists')
    @api.response(400, 'Number of boxes out of the allowed range')
    @api.expect(lockerset)
    @api.marshal_list_with(lockerset)
    def post(self):
        """
        Creates a new lockerset.
        """
        data = request.json
        lockerset = create_lockerset(data) 
        return lockerset, 201


@ns.route('/<int:id>')
@api.response(404, 'Lockerset not found.')
class LockersetItem(Resource):

    @api.marshal_list_with(lockerset)
    def get(self, id):
        """
        Returns a lockerset.
        """
        return Lockerset.query.filter(Lockerset.id == id).one()

#    @api.expect(lockerset)
#    @api.response(204, 'Lockerset successfully updated.')
#    def put(self, id):
#        """
#        Updates a Lockerset.
#
#        Use this method to change the Lockerset.
#
#        * Send a JSON object with the new name in the request body.
#
#        ```
#        {
#          "name": "New Category Name"
#        }
#        ```
#
#        * Specify the ID of the category to modify in the request URL path.
#        """
#        data = request.json
#        update_category(id, data)
#        return None, 204

    @api.response(204, 'Lockerset successfully deleted.')
    def delete(self, id):
        """
        Deletes a lockerset.
        """
        delete_lockerset(id)
        return None, 204
