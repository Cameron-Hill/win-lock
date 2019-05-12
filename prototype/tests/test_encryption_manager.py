import pytest
from win_lock import encryption_manager
from .defaults import *

def test_get_encryption_key():
    key = encryption_manager.get_key(password=config['password'].encode(), salt=test_salt)
    a=1
    assert key == derived_test_key