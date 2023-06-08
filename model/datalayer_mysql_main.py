import mysql.connector


class Datamanager:

    def __init__(self):

        self._user = "papi"
        self._hostname = "localhost"
        self._password = "qCMhi0K1L2gjBckYx54n"
        self._database = "stockbase"

    def init_conn(self):

        return mysql.connector.connect(user=self._user, host=self._hostname, password=self._password, database=self._database)

    def select(self, sqlstring):

        mydb = self.init_conn()
        mycursor = mydb.cursor(buffered=True)
        mycursor.execute(sqlstring)
        result = mycursor.fetchall()
        mydb.close()
        return result

    def query(self, sqlstring, val=None):

        mydb = self.init_conn()
        mycursor = mydb.cursor(buffered=True)

        if isinstance(val, list):
            mycursor.executemany(sqlstring, val)
        elif isinstance(val, tuple):
            mycursor.execute(sqlstring, val)
        elif not val:
            mycursor.execute(sqlstring)

        mydb.commit()
        mydb.close()
        return mycursor.rowcount
