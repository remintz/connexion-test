from smartlocker_api.database import db
from smartlocker_api.database.models import Lockerset

def create_lockerset(data):
    code = data.get('code')
    numBoxes = data.get('numBoxes')
    lockerset = Lockerset.query.filter(Lockerset.code == code).first()
    print('create_lockerset')
    print(lockerset)
    if lockerset is not None:
        raise ValueError('Cannot create lockersets with the same code')
    lockerset = Lockerset(code, numBoxes)
    db.session.add(lockerset)
    db.session.commit()
    return lockerset    

def delete_lockerset(lockerset_id):
    lockerset = Lockerset.query.filter(Lockerset.id == lockerset_id).one()
    db.session.delete(lockerset)
    db.session.commit()

