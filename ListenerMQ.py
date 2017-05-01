from pythonTestFramework.Loger.Loger import Loger
from pythonTestFramework.Generation.GenerationData import GenerationData
from pythonTestFramework.Serialization.ProtoBufSerializer import ProtoBufSerializer
import Queue
import time
from Config import Config
from AdapterMySQL import AdapterMySQL
from pythonTestFramework.Connectors.ConnectToMySQL import ConnectToMySQL
from threading import Thread
from datetime import datetime
import MySQLdb


class ListenerMQ():
    def __init__(self):
        self.confObj = Config()
        self._loger = Loger()
        self.__listQuotes = Queue.Queue()
        self.__listOrders = Queue.Queue()
        self.__serializer = ProtoBufSerializer()
        self.__gen = GenerationData()
        self.confObj.countAllElementsFromMQ = 0

    def start(self, mq, exchangeName, exchangeType, queueName, routingKey):
        try:
            #connect to mysql and clear tables
            self.adapterMySQL = ConnectToMySQL()
            self.cursor = self.adapterMySQL.connect(self.confObj.mySQL)
            self.cursor.execute(self.confObj.queryTruncateOrders)
            self.cursor.execute(self.confObj.queryTruncateQuotes)
            #start handler quotes
            handlerQuotes = Thread(target=self.__handlerQuotes)
            handlerQuotes.setDaemon(True)
            handlerQuotes.start()
            mq.start_consuming(exchangeName, exchangeType, queueName, routingKey, self.callbackReciveQuote)
        except Exception as ex:
            print ex.message
            self._loger.error(self, exception=ex)

    def callbackReciveQuote(self, ch, method, properties, body):
        try:
            marketDepthList = self.__serializer.deserialaze('MarketDepthList', body)
            for quote in marketDepthList['marketDepth']:
                quote['timeStampMDL'] = marketDepthList['timeStamp']/1000
                self.__listQuotes.put(quote)
                self.confObj.countAllElementsFromMQ += 1
        except Exception as ex:
            print ex.message
            self._loger.error(self, exception=ex)

    def __handlerQuotes(self):
        while True:
            time.sleep(1)
            #handler quotes
            if self.__listQuotes.qsize() >= self.confObj.countQuotesForOneOrder:
                listQuotes = []
                for i in range(0, self.confObj.countQuotesForOneOrder):
                    listQuotes.append(self.__listQuotes.get())
                    if i == self.confObj.countQuotesForOneOrder - 1:
                        order = self.__gen.generate_data('Order')
                        order['timeStamp'] = MySQLdb.TimestampFromTicks(int(order['timeStamp'] / 1000))
                        order['currencyPair'] = listQuotes[self.confObj.countQuotesForOneOrder - 1]['currencyPair']
                        if order['tradeType'] == 0:
                            order['filledPrice'] = listQuotes[self.confObj.countQuotesForOneOrder - 1]['bid']['quote'][0]['price']
                            order['filledVolume'] = listQuotes[self.confObj.countQuotesForOneOrder - 1]['bid']['quote'][0]['volume']
                        elif order['tradeType'] == 1:
                            order['filledPrice'] = listQuotes[self.confObj.countQuotesForOneOrder - 1]['offer']['quote'][0]['price']
                            order['filledVolume'] = listQuotes[self.confObj.countQuotesForOneOrder - 1]['offer']['quote'][0]['volume']
                        self.__listOrders.put(order)
                self.__saveQuotesToDB(listQuotes)
            #handler orders
            if self.__listOrders.qsize() >= self.confObj.countOrdersForSave:
                listOrders = []
                for i in range(0, self.confObj.countOrdersForSave):
                    listOrders.append(self.__listOrders.get())

                self.__saveOrdersToDB(listOrders)

    def __saveQuotesToDB(self, listQuotes):
        dataForQuery = []
        for i in range(0, len(listQuotes)):
            dataForQuery.append((MySQLdb.TimestampFromTicks(listQuotes[i]['timeStamp']),
                            listQuotes[i]['provider'],
                            listQuotes[i]['currencyPair'],
                            'BID',
                            listQuotes[i]['bid']['quote'][0]['volume'],
                            listQuotes[i]['bid']['quote'][0]['price'],
                            MySQLdb.TimestampFromTicks(listQuotes[i]['timeStampMDL'])))
            dataForQuery.append((MySQLdb.TimestampFromTicks(listQuotes[i]['timeStamp']),
                            listQuotes[i]['provider'],
                            listQuotes[i]['currencyPair'],
                            'OFFER',
                            listQuotes[i]['offer']['quote'][0]['volume'],
                            listQuotes[i]['offer']['quote'][0]['price'],
                            MySQLdb.TimestampFromTicks(listQuotes[i]['timeStampMDL'])))

        self.cursor.executemany(self.confObj.queryInsertQuotes, dataForQuery)
        self.adapterMySQL.disconnect()

    def __saveOrdersToDB(self, listOrders):
        dataForQuery = []
        for i in range(0, len(listOrders)):
            oneOrder = []
            for field in self.confObj.orderFillOrder:
                oneOrder.append(listOrders[i][field])
            dataForQuery.append(oneOrder)
        self.cursor.executemany(self.confObj.queryInsertOrders, dataForQuery)
        self.adapterMySQL.disconnect()
