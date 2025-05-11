from sqlbuilder.sql import Base, WillModifyData

class Delete(Base, WillModifyData):
    @classmethod
    def bind_placeholder(cls):
        return '?'

    def __init__(self):
        self._install_component('FROM')
        self._install_component('WHERE')
        self._install_component('ORDERBY')
        self._install_component('LIMIT')
        self._install_component('OFFSET')

    def FROM(self, *args):
        self._add_to_component(*args)
        return self
    
    def REPLACE_FROM(self, *args):
        self._empty_component()
        return self.FROM(*args)

    def WHERE(self, *args):
        self._add_to_component(*args)
        return self
    
    def REPLACE_WHERE(self, *args):
        self._empty_component()
        return self.WHERE(*args)

    def ORDERBY(self, *args):
        self._add_to_component(*args)
        return self
    
    def REPLACE_ORDERBY(self, *args):
        self._empty_component()
        return self.ORDERBY(*args)

    def LIMIT(self, *args):
        self._add_to_component(*args)
        return self
    
    def REPLACE_LIMIT(self, *args):
        self._empty_component()
        return self.LIMIT(*args)

    def OFFSET(self, *args):
        self._add_to_component(*args)
        return self
    
    def REPLACE_OFFSET(self, *args):
        self._empty_component()
        return self.OFFSET(*args)

    def to_sql_and_binds(self):
        SQL = ''
        BINDS = []

        if hasattr(self, '_PRE_VERBOSE') and len(getattr(self, '_PRE_VERBOSE')) > 0:
            SQL += ' '.join(getattr(self, '_PRE_VERBOSE')) + ' '
            BINDS = BINDS + getattr(self, '_PRE_VERBOSE_BINDS')


        if hasattr(self, '_FROM') and len(getattr(self, '_FROM')) > 0:
            SQL += 'DELETE FROM '

            SQL += ','.join(getattr(self, '_FROM'))
            BINDS = BINDS + getattr(self, '_FROM_BINDS')

        if hasattr(self, '_WHERE') and len(getattr(self, '_WHERE')) > 0:
            SQL += ' WHERE '

            SQL += ' AND '.join(getattr(self, '_WHERE'))
            BINDS = BINDS + getattr(self, '_WHERE_BINDS')

        if hasattr(self, '_ORDERBY') and len(getattr(self, '_ORDERBY')) > 0:
            SQL += ' ORDER BY '

            SQL += ','.join(getattr(self, '_ORDERBY'))
            BINDS = BINDS + getattr(self, '_ORDERBY_BINDS')

        if hasattr(self, '_LIMIT') and len(getattr(self, '_LIMIT')) > 0:
            SQL += ' LIMIT '

            SQL += ','.join(getattr(self, '_LIMIT'))
            BINDS = BINDS + getattr(self, '_LIMIT_BINDS')

        if hasattr(self, '_OFFSET') and len(getattr(self, '_OFFSET')) > 0:
            SQL += ' OFFSET '

            SQL += ','.join(getattr(self, '_OFFSET'))
            BINDS = BINDS + getattr(self, '_OFFSET_BINDS')

        if hasattr(self, '_POST_VERBOSE') and len(getattr(self, '_POST_VERBOSE')) > 0:
            SQL += ' '.join(getattr(self, '_POST_VERBOSE'))
            BINDS = BINDS + getattr(self, '_POST_VERBOSE_BINDS')

        return SQL, BINDS
    
    def execute(self, dbh):
        sql, binds = self.to_sql_and_binds()
        return self.modify_data(dbh, sql, binds)