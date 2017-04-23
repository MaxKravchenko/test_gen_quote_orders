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

    def start(self, mq, exchangeName, exchangeType, queueName, routingKey):
        try:
            mq.start_consuming(exchangeName, exchangeType, queueName, routingKey, self.callbackReciveQuote)

            # timer = Timer(self.confObj.waitListenerHandler, self.__handlerQuotes)
            # timer.start()
        except Exception as ex:
            print ex.message
            self._loger.error(self, exception=ex)

    def callbackReciveQuote(self, ch, method, properties, body):
        try:
            quote = self.__serializer.deserialaze('MarketDepth', body)
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
