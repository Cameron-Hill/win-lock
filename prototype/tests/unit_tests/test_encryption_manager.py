import os
import shutil
import pytest
from copy import deepcopy
from win_lock import encryption_manager
from prototype.tests.defaults import *

data_dir = os.path.join(os.path.dirname(__file__),os.pardir, 'test_data')

@pytest.fixture()
def manager():
    return encryption_manager.CryptManager(deepcopy(config), salt=test_salt)

def test_encryption_key_is_generated_correctly_from_string_password(manager):
    assert manager.key == derived_test_key

def test_encrypt_file(manager):
    file = os.path.join(data_dir,'test_text.txt')
    os.remove(file+'.wl') if os.path.isfile(file+'.wl' ) else None
    manager.encrypt_file(file)
    assert os.path.isfile(file+'.wl')

def test_decrypt_file(manager):
    encrpyted_file =os.path.join(data_dir, 'encrypted_data','test_text.txt.wl')
    with open(encrpyted_file, 'rb') as f:
        data = f.read()
    decrypted_bytes = manager.decrypt_bytes(data)
    with open(os.path.join(data_dir,'test_text.txt'), 'rb') as f:
        expected_bytes = f.read()
    assert expected_bytes == decrypted_bytes


def test_decrypt_data(manager):
    file = os.path.join(data_dir,'encrypted_data','test_text.txt.wl')
    expected_result = b"test file 1\r\nthis is a test of a basic text file"
    with open(file, 'rb') as f: bytes = f.read()
    result = manager.decrypt_bytes(bytes)
    assert result == expected_result

def test_encrypt_and_decrypt_bytes(manager):
    data = b'Plain Data'
    encrypted_data = manager.encrypt_bytes(data)
    assert isinstance(encrypted_data, bytes) and len(encrypted_data) > 0, 'Failed to successfully encrypt data'
    assert manager.decrypt_bytes(encrypted_data) == data, 'Failed to successfully decrypt data'


def test_encrypt_file_and_remove(manager):
    base_file = os.path.join(data_dir,'test_text.txt')
    test_file = base_file+'.2'
    shutil.copy(base_file,test_file)
    manager.encrypt_and_delete_file(test_file, passes=1)
    assert not os.path.exists(test_file)
    assert os.path.exists(test_file+'.wl')
    os.remove(test_file+'.wl')

def test_encrypt_file_and_remove_with_10_passes(manager):
    base_file = os.path.join(data_dir,'test_text.txt')
    test_file = base_file+'.2'
    shutil.copy(base_file,test_file)
    manager.encrypt_and_delete_file(test_file, passes=10)
    assert not os.path.exists(test_file)
    assert os.path.exists(test_file + '.wl')
    os.remove(test_file + '.wl')
