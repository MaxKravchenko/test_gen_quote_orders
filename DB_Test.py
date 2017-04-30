import unittest
import pythonTestFramework.Generation.GenerationData as gen
from pythonTestFramework.Connectors.ConnectToMySQL import ConnectToMySQL
from Config import Config

class list_test(unittest.TestCase):

    def test_time_save_quota(self):
        self.confObj = Config()

        self.adapterMySQL = ConnectToMySQL()
        self.cursor = self.adapterMySQL.connect(self.confObj.mySQL)
        query = 'SELECT AVG(UNIX_TIMESTAMP(create_time) - UNIX_TIMESTAMP(timeStampMDL)) FROM quotes;'
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        print 'Average time for save quota (s) = {0}'.format(round(result[0], 2))


    def test_metrics(self):
        self.confObj = Config()
        listQuery = {'maxPriceOrder': 'SELECT MAX(filledPrice) FROM orders',
                     'minPriceOrder': 'SELECT MIN(filledPrice) FROM orders',
                     'avgPriceOrder': 'SELECT AVG(filledPrice) FROM orders',
                     'maxVolumeOrder': 'SELECT MAX(filledVolume) FROM orders',
                     'minVolumeOrder': 'SELECT MIN(filledVolume) FROM orders',
                     'avgVolumeOrder': 'SELECT AVG(filledVolume) FROM orders',
                     'countOrders': 'SELECT COUNT(*) FROM orders'}
        self.adapterMySQL = ConnectToMySQL()
        self.cursor = self.adapterMySQL.connect(self.confObj.mySQL)

        for name, query in listQuery.items():
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            print 'dd {0} = {1}'.format(name, round(result[0], 2))
