from pythonTestFramework.Loger.Loger import Loger
from pythonTestFramework.Generation.GenerationData import GenerationData
import time
from Config import Config
import random

class GeneratorQuote():
    def __init__(self):
        self._loger = Loger()
        self.confObj = Config()
        self.__gen = GenerationData()
        self.confObj.countAllElementsToMQ = 0

    def genQuotes(self):
        try:
            self.startTime = int(time.time())
            self.currentTime = 0
            for second in range(0, self.confObj.totalTimeForGenerationQuotes):
                self.currentTime = self.startTime + second
                listQuotes = []
                for i in range(0, random.randint(self.confObj.countQuotesOnSecond['min'], self.confObj.countQuotesOnSecond['max'])):
                    quota = self.__gen.generate_data('MarketDepth')
                    quota['timeStamp'] = self.currentTime
                    listQuotes.append(quota)
                    self.confObj.countAllElementsToMQ += 1
                marketDepthList = self.__gen.generate_data('MarketDepthList')
                marketDepthList['marketDepth'] = listQuotes
                self.adapterMQ.publishMessage(marketDepthList)
        except Exception as ex:
            print ex.message
            self._loger.error(self, exception=ex)     

    def start(self, objAdapter):
        self.adapterMQ = objAdapter
        self.genQuotes()
