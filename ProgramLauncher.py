from pythonTestFramework.Launcher.Launcher import Launcher
from pythonTestFramework.Credentials.LoadCredentials import LoadCredentials
from GeneratorQuote import GeneratorQuote
import time
from Config import Config


class ProgramLauncher(Launcher):
    def start(self):
        try:
            self.confObj = Config()
            GeneratorQuote().start()
            Launcher().start()
        except Exception as ex:
            print ex.message

if __name__ == "__main__":
    LoadCredentials().set_name_config("CONF")
    ProgramLauncher().start()
