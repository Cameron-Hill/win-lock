import os
import pytest
from copy import deepcopy
from win_lock import encryption_manager
from .defaults import *

@pytest.fixture()
def manager():
    return encryption_manager.CryptManager(deepcopy(config), salt=test_salt)

def test_encryption_key_is_generated_correctly_from_string_password(manager):
    assert manager.key == derived_test_key

def test_encrypt_file(manager):
    file = r'test_data\test_text.txt'
    os.remove(file+'.wl') if os.path.isfile(file+'.wl' ) else None
    manager.encrypt_file(file)
    assert os.path.isfile(file+'.wl')



def test_encrypt_and_decrypt_bytes(manager):
    data = b'Plain Data'
    encrypted_data = manager.encrypt_bytes(data)
    assert isinstance(encrypted_data, bytes) and len(encrypted_data) > 0, 'Failed to successfully encrypt data'
    assert manager.decrypt_bytes(encrypted_data) == data, 'Failed to successfully decrypt data'


