from pythonTestFramework.Connectors.ConnectToMySQL import ConnectToMySQL
from pythonTestFramework.Loger.Loger import Loger
import MySQLdb

class AdapterMySQL(ConnectToMySQL):
    def __init__(self):
        self._loger = Loger()
        ConnectToMySQL.__init__(self)

    def executemany(self, query, args):
        try:
            self.__cursor.executemany(query, args)
        except Exception as ex:
            print ex.message
            self._loger().error(self, exception=ex)

    def execute(self, query, args):
        try:
            self.__cursor.execute(query, args)
        except Exception as ex:
            self._loger().error(self, exception=ex)
