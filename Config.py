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
        self.waitGenerator = 5
        # self.waitListenerHandler = 1.0
        self.countAllElementsToMQ = 0
        self.countAllElementsFromMQ = 0
        # self.countSendTimeForQuote = 0
        self.countReciveTotalTimeForQuote = 0
        self.countAVGTimeForQuote = 0
        self.countQuotesOnSecond = {'min': 30, 'max': 40}
        self.countQuotesForOneOrder = 100
        self.countOrdersForSave = 10
        # self.sizeQuota = 80
        # self.sizeOrder = 48
        self.totalTimeForGenerationQuotes = 3200
        # self.timeForGenerationQuotes = 1
        self.mySQL = {'host': '127.0.0.1',
              'port': 3306,
              'user': 'root',
              'password': 'cat',
              'db': 'trade_db'}
        self.queryTruncateOrders = """TRUNCATE TABLE orders"""
        self.queryTruncateQuotes = """TRUNCATE TABLE quotes"""
        self.queryInsertOrders = """INSERT INTO orders (timestamp,
                                                   status,
                                                   source_lp,
                                                   order_id,
                                                   initial_volume,
                                                   order_type,
                                                   trade_type,
                                                   currency_pair,
                                                   filledVolume,
                                                   initialPrice,
                                                   filledPrice)
                                                   VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        self.queryInsertQuotes = """INSERT INTO quotes (timestamp,
                                                        provider,
                                                        currency_pair,
                                                        type, volume,
                                                        price,
                                                        timeStampMDL)
                                                        VALUES (%s, %s, %s, %s, %s, %s, %s)"""
        self.orderFillOrder = ('timeStamp',
                               'status',
                               'sourceLp',
                               'orderId',
                               'initialVolume',
                               'orderType',
                               'tradeType',
                               'currencyPair',
                               'filledVolume',
                               'initialPrice',
                               'filledPrice')

        self.listQueryForTestMetrics = {'maxPriceOrder': 'SELECT MAX(filledPrice) FROM orders',
                     'minPriceOrder': 'SELECT MIN(filledPrice) FROM orders',
                     'avgPriceOrder': 'SELECT AVG(filledPrice) FROM orders',
                     'maxVolumeOrder': 'SELECT MAX(filledVolume) FROM orders',
                     'minVolumeOrder': 'SELECT MIN(filledVolume) FROM orders',
                     'avgVolumeOrder': 'SELECT AVG(filledVolume) FROM orders',
                     'countOrders': 'SELECT COUNT(*) FROM orders'}

        self.queryForTestTimeSaveQuota = {'avgTimeSaveQuota': 'SELECT AVG(UNIX_TIMESTAMP(create_time) - UNIX_TIMESTAMP(timeStampMDL)) FROM quotes',
                     'countQuotes': 'SELECT COUNT(*) FROM quotes'}
