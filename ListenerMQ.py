from pythonTestFramework.Loger.Loger import Loger
from pythonTestFramework.Generation.GenerationData import GenerationData
from pythonTestFramework.Serialization.ProtoBufSerializer import ProtoBufSerializer
import Queue
from threading import Timer
from Config import Config

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
            mq.start_consuming(exchangeName, exchangeType, queueName, routingKey, self.callbackReciveQuote)
        except Exception as ex:
            print ex.message
            self._loger.error(self, exception=ex)

    def callbackReciveQuote(self, ch, method, properties, body):
        try:
            marketDepthList = self.__serializer.deserialaze('MarketDepthList', body)
            for quote in marketDepthList['marketDepth']:
                self.__listQuotes.put(quote)
                self.confObj.countAllElementsFromMQ += 1
                print quote
        except Exception as ex:
            print ex.message
            self._loger.error(self, exception=ex)

    def __handlerQuotes(self):
        pass

    def __saveQuotesToDB(self):
        pass

    def __saveOrdersToDB(self):
        pass

    def __genOrders(self):
        return self.__gen.generate_data('Order')
