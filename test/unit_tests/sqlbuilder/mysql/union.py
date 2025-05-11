from sqlbuilder.mysql import Select, Union
import unittest

class TestCase(unittest.TestCase):
    def test_all(self):
        s1 = Select().SELECT('ONE').FROM('FOO')
        s2 = Select().SELECT('*').FROM('BAR').WHERE(['A = ?', 'B'])
        u = Union().UNION(
            ['??', s1],
            ['??', s2]
        )
        self.assertEqual(u.to_sql_and_binds(), ('SELECT ONE FROM FOO UNION SELECT * FROM BAR WHERE A = %s', ['B']))

if __name__ == '__main__':
    unittest.main()