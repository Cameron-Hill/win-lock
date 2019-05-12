import pytest
from win_lock import config_manager as con_man

test_config_location = r'D:\cambo\Docs\Projects\win-lock\prototype\configs\test_config.yaml'

def test_get_test_config():
    config = con_man.get_config(test_config_location)
    assert config['user'] == 'test_user'
    assert config['password'] == 'test_password'
    assert isinstance(config['log_dir'],str)
    assert config['log_level'] == 'debug'


