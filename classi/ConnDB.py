import sqlite3
from sqlite3 import Error

class ConnDB:
    
    conn = None

    def __init__(self, urlDB):
        try:
            self.conn = sqlite3.connect(urlDB)
        except Error as e:
            raise e

    def close(self):
        if self.conn:
            self.conn.close()

    def executeCommit(self, query):
        try:
            cur = self.conn.cursor()
            cur.execute(query)
        except Error as e:
            raise e