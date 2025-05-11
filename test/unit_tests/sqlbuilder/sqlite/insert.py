from sqlbuilder.sqlite import Insert
import unittest

class TestCase(unittest.TestCase):
    def test_all(self):
        sql = Insert().INTO('FOO', 'BAR')
        sql.COLUMNS('FIRST', 'SECOND')
        sql.VALUES('1', '2')

        self.assertEqual(sql.to_sql_and_binds(), ('INSERT INTO FOO (FIRST,SECOND) VALUES (1,2)', []))

if __name__ == '__main__':
    unittest.main()