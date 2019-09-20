import os
import sqlite3
from sqlite3 import Error
from sql_queries import *


class DB:

    def __init__(self, dbpath):
        create = True
        if os.path.isfile(dbpath):
            create = False
        self._conn = None; self._connect(dbpath)
        if create:
            self._create_table()

    def insert(self, data):
        c = self._conn.cursor()
        ins = INSERT.format(*data)
        c.execute(ins)
        self._conn.commit()

    def _create_table(self):
        if self._conn:
            c = self._conn.cursor()
            # Create table
            c.execute(CREATE_TABLE)
            self._conn.commit()

    def _connect(self, dbpath):
        self._conn = None
        try:
            self._conn = sqlite3.connect(dbpath)
        except Error as e:
            print(e)

    def close(self):
        if self._conn:
            self._conn.close()

