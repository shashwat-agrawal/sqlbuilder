import copy
class CanFetchResults():
    @classmethod
    def fetch_results(cls, dbh, sql, binds):
        cur = dbh.cursor()
        binds = tuple(binds)
        cur.execute(sql, binds)
        col_names = [x[0] for x in cur.description]
        ret = []
        for row in cur.fetchall():
            row_result = {}
            for col_index in range(len(col_names)):
                row_result[col_names[col_index]] = row[col_index]
            ret.append(copy.deepcopy(row_result))
        return ret