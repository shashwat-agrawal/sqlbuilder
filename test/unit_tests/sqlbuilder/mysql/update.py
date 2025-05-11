from sqlbuilder.mysql import Update
import unittest

class TestCase(unittest.TestCase):
    def test_all(self):
        sql = Update(
            ).UPDATE(
                'FOO'
            ).SET(
                ['A = ?', 'B']
            ).WHERE(
                ['ONE = ?', 1]
            )

        self.assertEqual(sql.to_sql_and_binds(), ('UPDATE FOO SET A = %s WHERE ONE = %s', ['B', 1]))

if __name__ == '__main__':
    unittest.main()