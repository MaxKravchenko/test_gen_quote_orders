from pythonTestFramework.Loger.Loger import Loger
from ListenerMQ import ListenerMQ
from pythonTestFramework.Generation.GenerationData import GenerationData
from pythonTestFramework.MQ.RabbitMQ import RabbitMQClient
from pythonTestFramework.Serialization.ProtoBufSerializer import ProtoBufSerializer
from threading import Thread
import time
from threading import Timer
from Config import Config
import random

class AdapterMQ():
    def __init__(self):
        self.confObj = Config()
        self._loger = Loger()
        self.__serializer = ProtoBufSerializer()

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

    def publishMessage(self, data):
        try:
            messageBody = self.__serializer.serialaze('MarketDepthList', data)
            self.mq.sendMessage(self.confObj.exchangeName, self.confObj.routingKey, messageBody)
        except Exception as ex:
            print ex.message
            self._loger.error(self, exception=ex)

    def disconnect(self):
        self.mq.disconnect()

    def start(self):
        self.__prepeareDB()
        self.__startListenerMQ()
