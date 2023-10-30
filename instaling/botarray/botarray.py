from ..bot import Bot
from multiprocessing import Process, Lock

class Botarray:
    def __init__(self, 
        path_to_words_json = None, 
        path_to_logfile = None,
        speedrun = False):

        self.path_to_words_json = path_to_words_json
        self.path_to_logfile = path_to_logfile
        self.lock = Lock()
        self.speedrun = speedrun

        self.botarray = []

    # append the botarray
    def append(self, login: str, passwd: str):
        self.botarray.append(Bot(
            login=login,
            passwd=passwd,

            lock=self.lock,
            path_to_words_json=self.path_to_words_json,
            path_to_logfile=self.path_to_logfile,
            speedrun=self.speedrun
        ))

    # start all the sessions simultaneously and wait for them
    def start(self):
        for bot in self.botarray:
            bot.proc = Process(target=bot.start)
            bot.proc.start()
        
        for bot in self.botarray:
            bot.proc.join()