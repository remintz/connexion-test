from smartlocker_api.database import db
from smartlocker_api.database.models import Lockerset, User
from smartlocker_api.util import ValidationError

def create_lockerset(data):
    code = data.get('code')
    numBoxes = data.get('numBoxes')
    lockerset = Lockerset.query.filter(Lockerset.code == code).first()
    print('create_lockerset')
    print(lockerset)
    if lockerset is not None:
        raise ValidationError('Cannot create lockersets with the same code', status_code=409)
    if numBoxes < 1:
        raise ValidationError('Number of boxes should be greater than 0', status_code=400)
    lockerset = Lockerset(code, numBoxes)
    db.session.add(lockerset)
    db.session.commit()
    return lockerset    

def delete_lockerset(lockerset_id):
    lockerset = Lockerset.query.filter(Lockerset.id == lockerset_id).one()
    db.session.delete(lockerset)
    db.session.commit()

