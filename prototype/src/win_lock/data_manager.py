import sqlite3

class DataManager():
    class TABLES:
        class SECURE_FOLDERS:
            NAME = "SECURE_FOLDERS"
            SCHEMA = """(id integer primary key autoincrement,
                        folder_path text not null,
                        created text,
                        last_accessed text)"""


    def __init__(self, database):
        self.conn = sqlite3.connect(database)
        self._initialise_connection()

    def _initialise_connection(self):
        self._initialise_table(DataManager.TABLES.SECURE_FOLDERS)

    def _initialise_table(self, table):
        sql = "CREATE TABLE IF NOT EXISTS {0} {1};".format(table.NAME, table.SCHEMA)
        cur = self.conn.cursor()
        cur.execute(sql)
        cur.close()

    def insert_secure_path(self, path):
        sql = 'INSERT INTO {} (folder_path, created, last_accessed) VALUES("{}", CURRENT_TIMESTAMP, CURRENT_TIMESTAMP)'.format(
            DataManager.TABLES.SECURE_FOLDERS.NAME, path)
        cur = self.conn.cursor()
        cur.execute(sql)
        cur.execute('commit;')
        cur.close()










