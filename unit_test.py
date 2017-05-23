import os
import app as application
import unittest
import tempfile
import settings
import json
import logging

TOKEN = 'abc'
LOCKER1_CODE = 'LOCKER1'
LOCKER1_NUM_BOXES = 10
LOCKER2_CODE = 'LOCKER2'
LOCKER2_NUM_BOXES = 20
LOCKER3_CODE = 'LOCKER3'

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

'''
class SmartLockerAPILockersetTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        log.debug('setUpClass')
        self.db_fd, self.db_file_name = tempfile.mkstemp()
        application.flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.db_file_name
        application.flask_app.config['TESTING'] = True
        self.app = application.flask_app.test_client()
        application.init_db(application.flask_app, True)

    @classmethod
    def tearDownClass(self):
        log.debug('tearDownClass')
        os.close(self.db_fd)
        os.unlink(self.db_file_name)

    def test_0100_lockerset_empty(self):
        response = self.app.get('/lockersets', headers={'token': TOKEN})
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data, [])

    def test_0200_create_lockerset_ok(self):
        response = self.app.post('/lockersets', \
            headers = { 'token': TOKEN, 'code': LOCKER1_CODE, 'numBoxes': LOCKER1_NUM_BOXES }        \
        )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['code'], LOCKER1_CODE)
        self.assertEqual(data['numBoxes'], LOCKER1_NUM_BOXES)

    def test_0300_create_lockerset_ok(self):
        response = self.app.post('/lockersets', \
            headers = { 'token': TOKEN, 'code': LOCKER2_CODE, 'numBoxes': LOCKER2_NUM_BOXES }        \
        )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['code'], LOCKER2_CODE)
        self.assertEqual(data['numBoxes'], LOCKER2_NUM_BOXES)

    def test_0400_list_lockersets(self):
        response = self.app.get('/lockersets', headers={'token': TOKEN})
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['code'], LOCKER1_CODE)
        self.assertEqual(data[0]['numBoxes'], LOCKER1_NUM_BOXES)
        self.assertEqual(data[1]['code'], LOCKER2_CODE)
        self.assertEqual(data[1]['numBoxes'], LOCKER2_NUM_BOXES)

    def test_0500_create_duplicate_lockerset(self):
        response = self.app.post('/lockersets', \
            headers = { 'token': TOKEN, 'code': LOCKER2_CODE, 'numBoxes': LOCKER2_NUM_BOXES }        \
        )
        self.assertEqual(response.status_code, 409)

    def test_0600_create_duplicate_lockerset_lowercase(self):
        response = self.app.post('/lockersets', \
            headers = { 'token': TOKEN, 'code': LOCKER2_CODE.lower(), 'numBoxes': LOCKER2_NUM_BOXES }        \
        )
        self.assertEqual(response.status_code, 409)
    
    def test_0700_create_lockerset_invalid_code(self):
        response = self.app.post('/lockersets', \
            headers = { 'token': TOKEN, 'code': 'Code with Spaces', 'numBoxes': LOCKER2_NUM_BOXES }        \
        )
        self.assertEqual(response.status_code, 400)

    def test_0800_create_lockerset_invalid_num_boxes(self):
        response = self.app.post('/lockersets', \
            headers = { 'token': TOKEN, 'code': LOCKER3_CODE, 'numBoxes': 0 }        \
        )
        self.assertEqual(response.status_code, 400)

    def test_0900_get_one_lockerset(self):
        response = self.app.get('/lockersets/' + LOCKER1_CODE, headers={'token': TOKEN})
        data = json.loads(response.get_data(as_text=True))
        log.debug('data: %s' % data)
        self.assertEqual(data['code'], LOCKER1_CODE)
        self.assertEqual(data['numBoxes'], LOCKER1_NUM_BOXES)

    def test_1000_delete_lockerset(self):
        response = self.app.delete('/lockersets/' + LOCKER1_CODE, \
            headers = { 'token': TOKEN }        \
        )
        self.assertEqual(response.status_code, 204)

    def test_1100_list_lockersets_after_delete(self):
        response = self.app.get('/lockersets', headers={'token': TOKEN})
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['code'], LOCKER2_CODE)
        self.assertEqual(data[0]['numBoxes'], LOCKER2_NUM_BOXES)
'''

class SmartLockerAPILockerboxTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        log.debug('setUpClass')
        self.db_fd, self.db_file_name = tempfile.mkstemp()
        application.flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.db_file_name
        application.flask_app.config['TESTING'] = True
        self.app = application.flask_app.test_client()
        application.init_db(application.flask_app, True)

    @classmethod
    def tearDownClass(self):
        log.debug('tearDownClass')
        os.close(self.db_fd)
        os.unlink(self.db_file_name)

    def test_0200_create_lockerset_ok(self):
        response = self.app.post('/lockersets', \
            headers = { 'token': TOKEN, 'code': LOCKER1_CODE, 'numBoxes': LOCKER1_NUM_BOXES }        \
        )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['code'], LOCKER1_CODE)
        self.assertEqual(data['numBoxes'], LOCKER1_NUM_BOXES)

    def test_0300_list_lockerboxes(self):
        response = self.app.get('/lockerbox/?lockersetCode=' + LOCKER1_CODE, \
            headers = { 'token': TOKEN }        \
        )
        data = json.loads(response.get_data(as_text=True))
   
        print ("data: %s" % data)

        self.assertEqual(len(data), LOCKER1_NUM_BOXES)
        for box in range(1, LOCKER1_NUM_BOXES):
            box_code = "%s/%d" % (LOCKER1_CODE, box)
            self.assertEqual(data[box-1]["lockerbox_code"], box_code)

if __name__ == '__main__':
    unittest.main()
