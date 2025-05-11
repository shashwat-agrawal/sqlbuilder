from sqlbuilder.sqlite.select import Select
import unittest

class TestCase(unittest.TestCase):
    def test_all(self):
        self.assertTrue(hasattr(Select, 'SELECT'))

        # ------- check all value errors
        with self.assertRaisesRegex(ValueError, 'add component encountered an argument which is not of type: .str, list.'):
            Select().SELECT(
                ()
            )


        with self.assertRaisesRegex(ValueError, 'binds found in string type argument. use list to supply bind values. see: abcdf ?'):
            Select().SELECT(
                'abcdf ?'
            )

        with self.assertRaisesRegex(ValueError, 'length should be greated than one for list arg type.'):
            Select().FROM(
                ['make it']
            )

        with self.assertRaisesRegex(ValueError, 'first element of list type argument should be string, but got: Select'):
            Select().FROM(
                [Select(), '1']
            )

        with self.assertRaisesRegex(ValueError, 'number of binds supplied for sql .ab = [?]. should be .1. but got .2.'):
            Select().WHERE(
                ['ab = ?', 1, 2]
            )

        with self.assertRaisesRegex(ValueError, 'bind mismatch at index 0 for sql arg .ab = [?].. Expected string or integer type bind'):
            Select().WHERE(
                ['ab = ?', [1, 2]]
            )

        with self.assertRaisesRegex(ValueError, 'bind mismatch at index 0 for sql arg .ab in ...... Expected list or nested sql type bind'):
            Select().WHERE(
                ['ab in (??)', 1]
            )

        self.assertEqual(Select().SELECT('foo', 'bar').to_sql_and_binds(), ('SELECT foo,bar', [])   )

        sql = Select(
            ).SELECT(
                'XYZ',
            ).WHERE(
                ['xyz = ?', 1]
            )
        self.assertEqual(sql.to_sql_and_binds(), ('SELECT XYZ WHERE xyz = ?', [1]))

        nest_sql = Select(
            ).SELECT(
                'NESTED ABC'
            ).FROM(
                'ABC_TABLE'
            ).WHERE(
                ['FOO IN (??)', [1, 2]]
            )

        sql = Select(
            ).SELECT(
                'BAR'
            ).FROM(
                ['(??) AS BAR_TABLE', nest_sql]
            ).WHERE(
                ['FOO_BAR = ?', 3]
            )

        self.assertEqual(sql.to_sql_and_binds(), ('SELECT BAR FROM (SELECT NESTED ABC FROM ABC_TABLE WHERE FOO IN (?,?)) AS BAR_TABLE WHERE FOO_BAR = ?', [1, 2, 3]))

        nest_sql.REPLACE_FROM(
            'FOO_TABLE'
        )
        self.assertEqual(nest_sql.to_sql_and_binds(), ('SELECT NESTED ABC FROM FOO_TABLE WHERE FOO IN (?,?)', [1, 2]))

if __name__ == '__main__':
    unittest.main()