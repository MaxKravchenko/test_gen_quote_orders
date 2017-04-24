from pythonTestFramework.Connectors.ConnectToMySQL import ConnectToMySQL


class AdapterMySQL(ConnectToMySQL):
    def __init__(self, confObj):
        ConnectToMySQL.__init__(self)

    def insert(self, query, args):
        try:
            self.__cursor.executemany(query, args)
        except Exception as ex:
            self._loger().error(self, exception=ex)

    def select(self, query, args):
        try:
            self.__cursor.execute(query, args)
        except Exception as ex:
            self._loger().error(self, exception=ex)
