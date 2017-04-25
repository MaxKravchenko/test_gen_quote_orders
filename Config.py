class Config(object):
    '''Contain parameters for program '''
    obj = None
    def __new__(cls, *args, **kwargs):
        if cls.obj is None:
            cls.obj = object.__new__(cls, *args, **kwargs)
        return cls.obj

    def __init__(self):
        #list parameters
        self.exchangeName = 'quote'
        self.exchangeType = 'direct'
        self.queueName = 'quote'
        self.routingKey = 'quote'
        self.waitGenerator = 3
        self.waitListenerHandler = 1.0
        self.countAllElementsToMQ = 0
        self.countAllElementsFromMQ = 0
        self.countQuotesOnSecond = {'min': 30, 'max': 40}
        self.countQuotesForOneOrder = 100
        self.countOrdersForSave = 5
        self.sizeQuota = 80
        self.sizeOrder = 48
        self.totalTimeForGenerationQuotes = 30
        self.timeForGenerationQuotes = 1
        self.mySQL = {'host': '127.0.0.1',
              'port': 3306,
              'user': 'root',
              'password': 'cat',
              'db': 'trade_db'}
