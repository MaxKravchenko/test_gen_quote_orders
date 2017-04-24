from pythonTestFramework.Generation.GenerationData import GenerationData
from pythonTestFramework.Credentials.LoadCredentials import LoadCredentials
from pythonTestFramework.Launcher.Launcher import Launcher
import time
import datetime
from threading import Timer


class myLauncher(Launcher):
    def start(self):
        try:
            self.gen = GenerationData()
            entity = self.gen.generate_data('Order')
            print entity
            # print entity['bid']['quote'][0]['volume']
            # print int(time.time())
            # print int(time.time()*1000)
            # print datetime.datetime.utcnow()

            # self.__timer = Timer(1, self.f)
            # self.__timer.start()

        except Exception as ex:
            print ex.message
    def f(self):
        print '1'

if __name__ == "__main__":
    LoadCredentials().set_name_config("CONF")
    myLauncher().start()
