from sqlbuilder.sql import Base, WillInsertData

class Insert(Base, WillInsertData):
    @classmethod
    def bind_placeholder(cls):
        return '?'

    def __init__(self):
        self._install_component('INTO')
        self._install_component('COLUMNS')
        self._install_component('VALUES')

    def INTO(self, *args):
        self._add_to_component(*args)
        return self
    
    def REPLACE_INTO(self, *args):
        self._empty_component()
        return self.INTO(*args)

    def COLUMNS(self, *args):
        self._add_to_component(*args)
        return self
    
    def REPLACE_COLUMNS(self, *args):
        self._empty_component()
        return self.COLUMNS(*args)

    def VALUES(self, *args):
        self._add_to_component(*args)
        return self
    
    def REPLACE_VALUES(self, *args):
        self._empty_component()
        return self.VALUES(*args)

    def to_sql_and_binds(self):
        SQL = ''
        BINDS = []

        if hasattr(self, '_PRE_VERBOSE') and len(getattr(self, '_PRE_VERBOSE')) > 0:
            SQL += ' '.join(getattr(self, '_PRE_VERBOSE')) + ' '
            BINDS = BINDS + getattr(self, '_PRE_VERBOSE_BINDS')

        SQL += 'INSERT INTO '

        if hasattr(self, '_INTO') and len(getattr(self, '_INTO')) > 0:
            SQL += getattr(self, '_INTO')[0]

        if hasattr(self, '_COLUMNS') and len(getattr(self, '_COLUMNS')) > 0:
            SQL += ' (' + ','.join(getattr(self, '_COLUMNS')) + ')'

        if hasattr(self, '_VALUES') and len(getattr(self, '_VALUES')) > 0:
            SQL += ' VALUES (' + ','.join(getattr(self, '_VALUES')) + ')'
            BINDS = BINDS + getattr(self, '_VALUES_BINDS')

        if hasattr(self, '_POST_VERBOSE') and len(getattr(self, '_POST_VERBOSE')) > 0:
            SQL += ' '.join(getattr(self, '_POST_VERBOSE'))
            BINDS = BINDS + getattr(self, '_POST_VERBOSE_BINDS')

        return SQL, BINDS
    
    def execute(self, dbh):
        sql, binds = self.to_sql_and_binds()
        return self.insert_data(dbh, sql, binds)