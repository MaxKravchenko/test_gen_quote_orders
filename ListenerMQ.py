from pythonTestFramework.Loger.Loger import Loger
from pythonTestFramework.Generation.GenerationData import GenerationData
from pythonTestFramework.Serialization.ProtoBufSerializer import ProtoBufSerializer
import Queue
import time
from Config import Config
from AdapterMySQL import AdapterMySQL
from pythonTestFramework.Connectors.ConnectToMySQL import ConnectToMySQL
from threading import Thread

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
            self.adapterMySQL = ConnectToMySQL()
            self.cursor = self.adapterMySQL.connect(self.confObj.mySQL)
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
                self.__listQuotes.put(quote)
                # print quote
                self.confObj.countAllElementsFromMQ += 1
        except Exception as ex:
            print ex.message
            self._loger.error(self, exception=ex)

    def __handlerQuotes(self):
        while True:
            time.sleep(1)
            if self.__listQuotes.qsize() >= self.confObj.countQuotesForOneOrder:
                listQuotes = []
                for i in range(0, self.confObj.countQuotesForOneOrder):
                    listQuotes.append(self.__listQuotes.get())
                    if i == self.confObj.countQuotesForOneOrder - 1:
                        order = self.__gen.generate_data('Order')
                        # order['timeStamp'] = int(order['timeStamp'] / 1000)
                        if order['tradeType'] == 0:
                            order['initialVolume'] = listQuotes[self.confObj.countQuotesForOneOrder - 1]['bid']['quote'][0]['volume']
                        elif order['tradeType'] == 1:
                            order['initialVolume'] = listQuotes[self.confObj.countQuotesForOneOrder - 1]['offer']['quote'][0]['volume']
                        self.__listOrders.put(order)

                self.__saveQuotesToDB(listQuotes)

            if self.__listOrders.qsize() >= self.confObj.countOrdersForSave:
                listOrders = []
                for i in range(0, self.confObj.countOrdersForSave):
                    listOrders.append(self.__listOrders.get())

                self.__saveOrdersToDB(listOrders)

    def __saveQuotesToDB(self, listQuotes):
        query = """INSERT INTO quotes    (timestamp, provider, currency_pair, type, volume, price) VALUES (%s, %s, %s, %s, %s, %s)"""
        dataForQuery = []
        for i in range(0, len(listQuotes)):
            dataForQuery.append((str(listQuotes[i]['timeStamp']),
                            listQuotes[i]['provider'],
                            listQuotes[i]['currencyPair'],
                            'BID',
                            listQuotes[i]['bid']['quote'][0]['volume'],
                            listQuotes[i]['bid']['quote'][0]['price']))
            dataForQuery.append((str(listQuotes[i]['timeStamp']),
                            listQuotes[i]['provider'],
                            listQuotes[i]['currencyPair'],
                            'OFFER',
                            listQuotes[i]['offer']['quote'][0]['volume'],
                            listQuotes[i]['offer']['quote'][0]['price']))

        self.cursor.executemany(query, dataForQuery)
        self.adapterMySQL.disconnect()

    def __saveOrdersToDB(self, listOrders):
        query = """INSERT INTO orders (timestamp, status, source_lp, order_id, initial_volume, order_type, trade_type, currency_pair) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        dataForQuery = []
        for i in range(0, len(listOrders)):
            dataForQuery.append((str(listOrders[i]['timeStamp']),
                            listOrders[i]['status'],
                            listOrders[i]['sourceLp'],
                            listOrders[i]['orderId'],
                            listOrders[i]['initialVolume'],
                            listOrders[i]['orderType'],
                            listOrders[i]['tradeType'],
                            listOrders[i]['currencyPair']))

        self.cursor.executemany(query, dataForQuery)
        self.adapterMySQL.disconnect()
