from pythonTestFramework.Loger.Loger import Loger
from ListenerMQ import ListenerMQ
from pythonTestFramework.Generation.GenerationData import GenerationData
from pythonTestFramework.MQ.RabbitMQ import RabbitMQClient
from pythonTestFramework.Serialization.ProtoBufSerializer import ProtoBufSerializer
from threading import Thread
import time
from threading import Timer
from Config import Config


class GeneratorQuote():
    def __init__(self):
        self._loger = Loger()
        self.confObj = Config()
        self.__gen = GenerationData()
        self.__serializer = ProtoBufSerializer()

    def __startListenerMQ(self):
        try:
            listener = Thread(target=ListenerMQ().start, args=(self.mq,
                                                               self.confObj.exchangeName,
                                                               self.confObj.exchangeType,
                                                               self.confObj.queueName,
                                                               self.confObj.routingKey))
            listener.setDaemon(True)
            listener.start()
        except Exception as ex:
            print ex.message
            self._loger.error(self, exception=ex)

    def __prepeareDB(self):
        try:
            self.mq = RabbitMQClient()
            self.mq.connect()
            self.mq.createExchange(self.confObj.exchangeName, self.confObj.exchangeType)
            self.mq.createQueue(self.confObj.queueName)
            self.mq.bindQueue(self.confObj.exchangeName, self.confObj.queueName, self.confObj.routingKey)
        except Exception as ex:
            print ex.message
            self._loger.error(self, exception=ex)

    def genQuotes(self):
        try:
            self.__startTime = time.time()
            currentTime = time.time()
            if currentTime - self.__startTime < self.confObj.totalTimeForGenerationQuotes:
                for i in range(1, self.confObj.countQuotesOnSecond):
                    self.__publishMessage(self.__gen.generate_data('MarketDepth'))
                    self.confObj.countAllElementsToMQ += 1

    def __publishMessage(self, data):
        try:
            messageBody = self.__serializer.serialaze('MarketDepth', data)
            self.mq.sendMessage(self.confObj.exchangeName, self.confObj.routingKey, messageBody)
        except Exception as ex:
            print ex.message
            self._loger.error(self, exception=ex)

    def start(self):
        self.__prepeareDB()
        self.__startListenerMQ()
        self.genQuotes()
        time.sleep(self.confObj.waitGenerator)
        self.mq.disconnect()
