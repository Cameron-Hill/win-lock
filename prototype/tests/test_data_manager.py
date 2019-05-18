import os
import pytest
from win_lock.data_manager import DataManager
from .defaults import *
import sqlite3

test_database = config['database']

@pytest.fixture
def manager():
    conn = sqlite3.connect(test_database)
    conn.execute("DROP TABLE IF EXISTS {}".format(DataManager.TABLES.SECURE_FOLDERS.NAME))
    conn.close()
    yield DataManager(test_database)

def test_secure_folder_table_name():
    assert DataManager.TABLES.SECURE_FOLDERS.NAME == "SECURE_FOLDERS"

def test_initalise_connection():
    conn = sqlite3.connect(test_database)
    conn.execute("DROP TABLE IF EXISTS {}".format(DataManager.TABLES.SECURE_FOLDERS.NAME))
    conn.close()
    DataManager(test_database)
    conn = sqlite3.connect(test_database)
    res = conn.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
    assert any([DataManager.TABLES.SECURE_FOLDERS.NAME in x for x in list(res)])
    conn.close()

def test_insert_secure_path(manager):
    manager.insert_secure_path(r'test\path')
    conn = sqlite3.connect(test_database)
    sql = "select * from {}".format(DataManager.TABLES.SECURE_FOLDERS.NAME)
    res = conn.execute(sql)
    res = [x for x in list(res)]
    a=1



