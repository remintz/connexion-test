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

USER1_EMAIL = 'user1@email.com'
USER1_PASSWORD = 'password1'
USER2_EMAIL = 'user2@email.com'
USER2_PASSWORD = 'password2'

ASSIGN_KEY_1 = '123'

locker_key = ''

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

class SmartLockerAPILockersetTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        log.debug('setUpClass')
        self.db_fd, self.db_file_name = tempfile.mkstemp()
        application.flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + self.db_file_name
        application.flask_app.config['TESTING'] = True
        application.flask_app.config['DEBUG'] = False
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

class SmartLockerApiUserTest(unittest.TestCase):
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

    def test_0100_list_users_empty(self):
        response = self.app.get('/users', headers={'token': TOKEN})
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data, [])

    def test_0200_create_user(self):
        response = self.app.post('/users', \
            headers = { 'token': TOKEN, 'email': USER1_EMAIL, 'password': USER1_PASSWORD }        \
        )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['email'], USER1_EMAIL)
        self.assertIsNone(data.get('password'))
        
    def test_0300_create_second_user(self):
        response = self.app.post('/users', \
            headers = { 'token': TOKEN, 'email': USER2_EMAIL, 'password': USER2_PASSWORD }        \
        )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['email'], USER2_EMAIL)
        self.assertIsNone(data.get('password'))

    def test_0400_list_two_users(self):
        response = self.app.get('/users', headers={'token': TOKEN})
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['email'], USER1_EMAIL)
        self.assertEqual(data[1]['email'], USER2_EMAIL)

    def test_0410_create_user_wrong_email(self):
        response = self.app.post('/users', \
            headers = { 'token': TOKEN, 'email': "abc", 'password': USER2_PASSWORD }        \
        )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 400)

    def test_0420_create_user_duplicate_email(self):
        response = self.app.post('/users', \
            headers = { 'token': TOKEN, 'email': USER2_EMAIL, 'password': USER2_PASSWORD }        \
        )
        self.assertEqual(response.status_code, 409)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['code'], 'DUP_USER')

    def test_0430_list_two_users_again(self):
        response = self.app.get('/users', headers={'token': TOKEN})
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['email'], USER1_EMAIL)
        self.assertEqual(data[1]['email'], USER2_EMAIL)

    def test_0440_get_one_user(self):
        response = self.app.get(('/users/%s' % USER2_EMAIL), headers={'token': TOKEN})
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 201, ('data: %s' % data))
        self.assertEqual(data['email'], USER2_EMAIL, ('data: %s' % data))

    def test_0500_delete_user(self):
        response = self.app.delete('/users/' + USER1_EMAIL, \
            headers = { 'token': TOKEN }        \
        )
        self.assertEqual(response.status_code, 204)

    def test_0550_delete_user_again(self):
        response = self.app.delete('/users/' + USER1_EMAIL, \
            headers = { 'token': TOKEN }        \
        )
        self.assertEqual(response.status_code, 204)

    def test_0600_list_one_user(self):
        response = self.app.get('/users', headers={'token': TOKEN})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['email'], USER2_EMAIL)


    def test_0700_delete_last_user(self):
        response = self.app.delete('/users/' + USER2_EMAIL, \
            headers = { 'token': TOKEN }        \
        )
        self.assertEqual(response.status_code, 204)

    def test_0800_list_no_users_again(self):
        response = self.app.get('/users', headers={'token': TOKEN})
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data, [])

    def test_0900_get_one_user_fail(self):
        response = self.app.get(('/users/%s' % USER2_EMAIL), headers={'token': TOKEN})
        self.assertEqual(response.status_code, 404)


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
        response = self.app.get(('/lockerbox?lockersetcode=%s' % LOCKER1_CODE), \
            headers = { 'token': TOKEN }        \
        )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data), LOCKER1_NUM_BOXES)
        for box in range(1, LOCKER1_NUM_BOXES):
            box_code = "%s/%d" % (LOCKER1_CODE, box)
            self.assertEqual(data[box-1]["lockerbox_code"], box_code)
            self.assertEqual(data[box-1]["status"], 0)

    def test_0500_list_lockerboxes_wrong_lockerset(self):
        response = self.app.get(('/lockerbox?lockersetcode=%s' % LOCKER2_CODE), \
            headers = { 'token': TOKEN }        \
        )
        data = json.loads(response.get_data(as_text=True))
        print ("data: %s" % data)
        self.assertEqual(len(data), 0)

class SmartLockerAPIBlueSkyScenario(unittest.TestCase):

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

    #--- create user
    #--- create lockerset
    #--- user login
    #--- user allocates a box
    #--- user closes box
    #--- user opens box with key
    #--- box is released

    def test_0100_create_user(self):
        response = self.app.post('/users', \
            headers = { 'token': TOKEN, 'email': USER1_EMAIL, 'password': USER1_PASSWORD }        \
        )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['email'], USER1_EMAIL)
        self.assertIsNone(data.get('password'))

    def test_0200_create_lockerset_ok(self):
        response = self.app.post('/lockersets', \
            headers = { 'token': TOKEN, 'code': LOCKER1_CODE, 'numBoxes': LOCKER1_NUM_BOXES }        \
        )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(data['code'], LOCKER1_CODE)
        self.assertEqual(data['numBoxes'], LOCKER1_NUM_BOXES)

    def test_0300_list_lockerboxes(self):
        response = self.app.get(('/lockerbox?lockersetcode=%s' % LOCKER1_CODE), \
            headers = { 'token': TOKEN }        \
        )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data), LOCKER1_NUM_BOXES)
        for box in range(1, LOCKER1_NUM_BOXES+1):
            box_code = "%s/%d" % (LOCKER1_CODE, box)
            self.assertEqual(data[box-1]["lockerbox_code"], box_code)

    def test_0310_get_lockerbox_key_unassigned(self):
        response = self.app.get('lockerboxkey?lockerboxcode=%s/%d&key=%s' % (LOCKER1_CODE, 2, '123'))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 409, ('data: %s' % data))
        self.assertEqual(data['code'], 'CANT_OPEN_LOCKERBOX')

    def test_0400_assign_box_to_user(self):
        global locker_key
        response = self.app.put("/lockerbox?lockerboxcode=%s/%d&user=%s&operation=Assign" % (LOCKER1_CODE, 2, USER1_EMAIL), \
            headers = { 'token': TOKEN }        \
        )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200, ('data: %s' % data))
        self.assertEqual(data['lockerbox_code'], ('%s/%d' % (LOCKER1_CODE, 2)))
        self.assertEqual(data['user'], USER1_EMAIL)
        self.assertIsNotNone(data.get('key'))
        self.assertNotEqual(len(data['key']), 0)
        self.assertEqual(data['key'], ASSIGN_KEY_1)
        self.assertEqual(data['status'], 1)
        locker_key = data['key']
        print('locker_key: %s' % locker_key)

    def test_0410_get_lockerbox_key(self):
        global locker_key
        response = self.app.get('lockerboxkey?lockerboxcode=%s/%d&key=%s' % (LOCKER1_CODE, 2, locker_key))
        self.assertEqual(response.status_code, 200)

    def test_0420_get_lockerbox_key_wrong_key(self):
        response = self.app.get('lockerboxkey?lockerboxcode=%s/%d&key=%s' % (LOCKER1_CODE, 2, 'aaaaa'))
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 409, ('data: %s' % data))
        self.assertEqual(data['code'], 'INVALID_KEY')

    def test_0500_list_available_boxes_after_assignment(self):
        # box #2 should be missing
        response = self.app.get(('/lockerbox?lockersetcode=%s&onlyavailable=True' % LOCKER1_CODE), \
            headers = { 'token': TOKEN }        \
        )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200, ('data: %s' % data))
        self.assertEqual(len(data), LOCKER1_NUM_BOXES-1, ('data: %s' % data))
        data_index = 0
        box_number = 1
        while box_number <= LOCKER1_NUM_BOXES:
            if box_number == 2:
                box_number = box_number + 1
            box_code = "%s/%d" % (LOCKER1_CODE, box_number)
            self.assertEqual(data[data_index]["lockerbox_code"], box_code, ('data: %s' % data))
            box_number = box_number + 1
            data_index = data_index + 1

    def test_0600_open_box_wrong_key(self):
        response = self.app.put("/lockerbox?lockerboxcode=%s/%d&user=%s&operation=Open&key=%s" % (LOCKER1_CODE, 2, USER1_EMAIL, 'wrongkey'), \
            headers = { 'token': TOKEN }        \
        )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 403, ('data: %s' % data))

    def test_0700_open_box_missing_key(self):
        response = self.app.put("/lockerbox?lockerboxcode=%s/%d&user=%s&operation=Open" % (LOCKER1_CODE, 2, USER1_EMAIL), \
            headers = { 'token': TOKEN }        \
        )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 400, ('data: %s' % data))

    def test_0800_open_box(self):
        global locker_key
        print('Locker key: %s' % locker_key)
        response = self.app.put("/lockerbox?lockerboxcode=%s/%d&user=%s&operation=Open&key=%s" % (LOCKER1_CODE, 2, USER1_EMAIL, locker_key), \
            headers = { 'token': TOKEN }        \
        )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200, ('data: %s' % data))

    def test_0900_unassign_box(self):
        response = self.app.put("/lockerbox?lockerboxcode=%s/%d&user=%s&operation=Unassign" % (LOCKER1_CODE, 2, USER1_EMAIL), \
            headers = { 'token': TOKEN }        \
        )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200, ('data: %s' % data))

    def test_1000_list_lockerboxes_after_unassign(self):
        response = self.app.get(('/lockerbox?lockersetcode=%s' % LOCKER1_CODE), \
            headers = { 'token': TOKEN }        \
        )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data), LOCKER1_NUM_BOXES)
        for box in range(1, LOCKER1_NUM_BOXES+1):
            box_code = "%s/%d" % (LOCKER1_CODE, box)
            self.assertEqual(data[box-1]["lockerbox_code"], box_code)

    def test_1100_open_unassigned_box(self):
        global locker_key
        print('Locker key: %s' % locker_key)
        response = self.app.put("/lockerbox?lockerboxcode=%s/%d&user=%s&operation=Open&key=%s" % (LOCKER1_CODE, 2, USER1_EMAIL, locker_key), \
            headers = { 'token': TOKEN }        \
        )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 409, ('data: %s' % data))
        
    def test_1200_assign_box_to_user_for_block_tests(self):
        global locker_key
        response = self.app.put("/lockerbox?lockerboxcode=%s/%d&user=%s&operation=Assign" % (LOCKER1_CODE, 2, USER1_EMAIL), \
            headers = { 'token': TOKEN }        \
        )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200, ('data: %s' % data))
        self.assertEqual(data['lockerbox_code'], ('%s/%d' % (LOCKER1_CODE, 2)))
        self.assertEqual(data['user'], USER1_EMAIL)
        self.assertIsNotNone(data.get('key'))
        self.assertNotEqual(len(data['key']), 0)
        self.assertEqual(data['key'], ASSIGN_KEY_1)
        self.assertEqual(data['status'], 1)
        locker_key = data['key']
        print('locker_key: %s' % locker_key)

    def test_1300_unblock_assigned_box(self):
        response = self.app.put("/lockerbox?lockerboxcode=%s/%d&user=%s&operation=Unblock" % (LOCKER1_CODE, 2, USER1_EMAIL), \
            headers = { 'token': TOKEN }        \
        )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 409, ('data: %s' % data))

    def test_1400_block_assigned_box(self):
        response = self.app.put("/lockerbox?lockerboxcode=%s/%d&user=%s&operation=Block" % (LOCKER1_CODE, 2, USER1_EMAIL), \
            headers = { 'token': TOKEN }        \
        )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 409, ('data: %s' % data))

    def test_1500_force_block_assigned_box(self):
        response = self.app.put("/lockerbox?lockerboxcode=%s/%d&user=%s&operation=BlockForced" % (LOCKER1_CODE, 2, USER1_EMAIL), \
            headers = { 'token': TOKEN }        \
        )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200, ('data: %s' % data))

    def test_1600_list_available_boxes_after_block(self):
        # box #2 should be missing
        response = self.app.get(('/lockerbox?lockersetcode=%s&onlyavailable=True' % LOCKER1_CODE), \
            headers = { 'token': TOKEN }        \
        )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200, ('data: %s' % data))
        self.assertEqual(len(data), LOCKER1_NUM_BOXES-1, ('data: %s' % data))
        data_index = 0
        box_number = 1
        while box_number <= LOCKER1_NUM_BOXES:
            if box_number == 2:
                box_number = box_number + 1
            box_code = "%s/%d" % (LOCKER1_CODE, box_number)
            self.assertEqual(data[data_index]["lockerbox_code"], box_code, ('data: %s' % data))
            box_number = box_number + 1
            data_index = data_index + 1

    def test_1700_unblock_box(self):
        response = self.app.put("/lockerbox?lockerboxcode=%s/%d&user=%s&operation=Unblock" % (LOCKER1_CODE, 2, USER1_EMAIL), \
            headers = { 'token': TOKEN }        \
        )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 200, ('data: %s' % data))

    def test_1800_list_lockerboxes_after_unblock(self):
        response = self.app.get(('/lockerbox?lockersetcode=%s' % LOCKER1_CODE), \
            headers = { 'token': TOKEN }        \
        )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(len(data), LOCKER1_NUM_BOXES)
        for box in range(1, LOCKER1_NUM_BOXES+1):
            box_code = "%s/%d" % (LOCKER1_CODE, box)
            self.assertEqual(data[box-1]["lockerbox_code"], box_code)
        
    def test_1900_invalid_operation(self):
        response = self.app.put("/lockerbox?lockerboxcode=%s/%d&user=%s&operation=XXXX" % (LOCKER1_CODE, 2, USER1_EMAIL), \
            headers = { 'token': TOKEN }        \
        )
        data = json.loads(response.get_data(as_text=True))
        self.assertEqual(response.status_code, 400, ('data: %s' % data))

def suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(SmartLockerApiUserTest))
    suite.addTest(unittest.makeSuite(SmartLockerAPILockersetTest))
    suite.addTest(unittest.makeSuite(SmartLockerAPILockerboxTest))
    suite.addTest(unittest.makeSuite(SmartLockerAPIBlueSkyScenario))
    return suite
    
if __name__ == '__main__':
#    unittest.main()
    runner = unittest.TextTestRunner()
    test_suite = suite()
    runner.run(test_suite)