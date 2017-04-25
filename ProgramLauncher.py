from pythonTestFramework.Launcher.Launcher import Launcher
from pythonTestFramework.Credentials.LoadCredentials import LoadCredentials
from GeneratorQuote import GeneratorQuote
from AdapterMQ import AdapterMQ
import time
from Config import Config

class ProgramLauncher(Launcher):
    def start(self):
        try:
            self.confObj = Config()
            self.adapterMQ = AdapterMQ()
            self.adapterMQ.start()
            GeneratorQuote().start(self.adapterMQ)
            time.sleep(5)
            Launcher().start()
            self.adapterMQ.disconnect()
        except Exception as ex:
            print ex.message

if __name__ == "__main__":
    LoadCredentials().set_name_config("CONF")
    ProgramLauncher().start()
