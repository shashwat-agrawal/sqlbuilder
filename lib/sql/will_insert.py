class WillInsertData():
    @classmethod
    def insert_data(cls, dbh, sql, binds):
        cur = dbh.cursor()
        binds = tuple(binds)
        cur.execute(sql, binds)
        return cur.lastrowid