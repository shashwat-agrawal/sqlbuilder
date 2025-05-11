from sqlbuilder.sqlite import Insert, Select
from test.util import testdir, mkpath_tree_fatal
import os
import sqlite3
import unittest

class TestCase(unittest.TestCase):
    def test_all(self):
        tdir = testdir()
        mkpath_tree_fatal(tdir, {})

        dbh = sqlite3.connect(os.path.join(tdir, 'test.db'), autocommit = True)
        cur = dbh.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS EMPLOYEE (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            NAME VARCHAR(50) NOT NULL
        );''')
        insert = Insert().INTO('EMPLOYEE').COLUMNS('NAME').VALUES(['??', ['FIRST']])
        insert.execute(dbh)
    
        sql = Select().SELECT('*').FROM('EMPLOYEE')
        results = sql.execute(dbh)
        self.assertEqual(results, [{'ID': 1, 'NAME': 'FIRST'}])

        sql = Select().SELECT('*').FROM('EMPLOYEE').WHERE(['NAME = ?', 'BAR'])
        results = sql.execute(dbh)
        self.assertEqual(results, [])

        dbh.close()

if __name__ == '__main__':
    unittest.main()