import time
import os
import shutil
from copy import deepcopy
from prototype.tests.defaults import *
from win_lock import encryption_manager
from win_lock import wl_builder


base_file = os.path.join(os.path.dirname(__file__),'test_text.txt')
salt = b'new_salt'

def time_test(func):
    def inner(*args, **kwargs):
        t1 = time.time()
        val = func(*args, **kwargs)
        print("Executed Test: {} in {}s".format(func.__name__, time.time()-t1))
        return val
    return inner

@time_test
def test_encrypt_and_build():
    manager = encryption_manager.CryptManager(deepcopy(config), salt=test_salt)
    test_file = base_file.replace('text','temp')
    shutil.copy(base_file,test_file)
    encrypted_file_path = manager.encrypt_and_delete_file(test_file)
    exe = wl_builder.build(encrypted_file_path)



