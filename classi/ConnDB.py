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

    def executeCommit(self, query, parms=()):
        try:
            cur = self.conn.cursor()
            cur.execute(query, parms)
            self.conn.commit()
            return cur.lastrowid
        except Error as e:
            raise e

    def execute(self, query):
        try:
            cur = self.conn.cursor()
            cur.execute(query)
        except Error as e:
            raise e
        
    def executeFetchAll(self, query):
        try:
            cur = self.conn.cursor()
            cur.execute(query)
            return cur.fetchall()
        except Error as e:
            raise e