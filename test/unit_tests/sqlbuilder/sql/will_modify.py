from sqlbuilder.sqlite import Insert, Select, Update, Delete
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
    
        select_sql = Select().SELECT('*').FROM('EMPLOYEE')
        results = select_sql.execute(dbh)
        self.assertEqual(results, [{'ID': 1, 'NAME': 'FIRST'}])

        update_sql = Update().UPDATE('EMPLOYEE').SET(['NAME = ?', 'SECOND'])
        update_sql.execute(dbh)

        results = select_sql.execute(dbh)
        self.assertEqual(results, [{'ID': 1, 'NAME': 'SECOND'}])

        delete_sql = Delete().FROM('EMPLOYEE').WHERE(['ID = ?', 2])
        delete_sql.execute(dbh)

        results = select_sql.execute(dbh)
        self.assertEqual(results, [{'ID': 1, 'NAME': 'SECOND'}])

        delete_sql.REPLACE_WHERE(['ID = ?', 1])
        delete_sql.execute(dbh)

        results = select_sql.execute(dbh)
        self.assertEqual(results, [])

        dbh.close()

if __name__ == '__main__':
    unittest.main()