from sqlbuilder.mysql import Delete
import unittest

class TestCase(unittest.TestCase):
    def test_all(self):
        sql = Delete(
            ).FROM(
                'FOO'
            ).WHERE(
                ['ONE = ?', 1]
            )

        self.assertEqual(sql.to_sql_and_binds(), ('DELETE FROM FOO WHERE ONE = %s', [1]))

if __name__ == '__main__':
    unittest.main()