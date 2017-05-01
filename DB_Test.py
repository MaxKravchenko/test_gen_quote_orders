import unittest
import pythonTestFramework.Generation.GenerationData as gen
from pythonTestFramework.Connectors.ConnectToMySQL import ConnectToMySQL
from Config import Config

class list_test(unittest.TestCase):

    def test_time_save_quota(self):
        self.confObj = Config()

        self.adapterMySQL = ConnectToMySQL()
        self.cursor = self.adapterMySQL.connect(self.confObj.mySQL)
        self.cursor.execute(self.confObj.queryForTestTimeSaveQuota)
        result = self.cursor.fetchone()
        print''
        print 'Average time for save quota (s) = {0}'.format(round(result[0], 2))

    def test_metrics(self):
        self.confObj = Config()
        self.adapterMySQL = ConnectToMySQL()
        self.cursor = self.adapterMySQL.connect(self.confObj.mySQL)

        print''
        for name, query in self.confObj.listQueryForTestMetrics.items():
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            print '{0} = {1}'.format(name, round(result[0], 2))
