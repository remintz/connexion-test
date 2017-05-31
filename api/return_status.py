ret_status = {}

def def_ret_status(mnemonic, message):
    ret_status[mnemonic] = { 'code': mnemonic, 'msg': message }

def get_ret_status(mnemonic):
    return ret_status[mnemonic]

def_ret_status('DUP_USER', 'ERROR: User already exists')
def_ret_status('USER_NOT_FOUND', 'ERROR: User already exists')
def_ret_status('LOCKERBOX_NOT_FOUND', 'ERROR: Locker box not found')
def_ret_status('CANT_OPEN_LOCKERBOX', 'ERROR: Locker box cannot be opened')
def_ret_status('INVALID_KEY', 'ERROR: Invalid key')

def_ret_status('USER_DELETED', 'OK: User deleted')

