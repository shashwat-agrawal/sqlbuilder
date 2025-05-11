from sqlbuilder.sql import Base, CanFetchResults

class UnionAll(Base, CanFetchResults):
    @classmethod
    def bind_placeholder(cls):
        return '%s'

    def __init__(self):
        self._install_component('UNION')

    def UNION(self, *args):
        self._add_to_component(*args)
        return self
    
    def REPLACE_UNION(self, *args):
        self._empty_component()
        return self.UNION(*args)

    def to_sql_and_binds(self):
        SQL = ''
        BINDS = []

        if hasattr(self, '_PRE_VERBOSE') and len(getattr(self, '_PRE_VERBOSE')) > 0:
            SQL += ' '.join(getattr(self, '_PRE_VERBOSE')) + ' '
            BINDS = BINDS + getattr(self, '_PRE_VERBOSE_BINDS')

        if hasattr(self, '_UNION') and len(getattr(self, '_UNION')) > 0:
            SQL += ' UNION ALL '.join(getattr(self, '_UNION'))
            BINDS = BINDS + getattr(self, '_UNION_BINDS')

        if hasattr(self, '_POST_VERBOSE') and len(getattr(self, '_POST_VERBOSE')) > 0:
            SQL += ' '.join(getattr(self, '_POST_VERBOSE'))
            BINDS = BINDS + getattr(self, '_POST_VERBOSE_BINDS')

        return SQL, BINDS
    
    def execute(self, dbh):
        sql, binds = self.to_sql_and_binds()
        return self.fetch_results(dbh, sql, binds)
