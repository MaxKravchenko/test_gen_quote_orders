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
            for i in range(0, self.confObj.totalTimeForGenerationQuotes):
                listQuotes = []
                for i in range(0, random.randint(self.confObj.countQuotesOnSecond['min'], self.confObj.countQuotesOnSecond['max'])):
                    quota = self.__gen.generate_data('MarketDepth')
                    listQuotes.append(quota)
                    self.confObj.countAllElementsToMQ += 1
                marketDepthList = {
                    'timeStamp': int(time.time()),
                    'nodeId': 'test',
                    'unitName': 'unit1',
                    'instanceId': 'test',
                    'marketDepth': listQuotes
                }
                self.adapterMQ.publishMessage(marketDepthList)
                time.sleep(1)
        except Exception as ex:
            print ex.message
            self._loger.error(self, exception=ex)


    def start(self, objAdapter):
        self.adapterMQ = objAdapter
        self.genQuotes()
