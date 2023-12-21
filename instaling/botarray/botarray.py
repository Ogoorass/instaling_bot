from ..bot import Bot
from random import randrange
from threading import Thread, Lock


class Botarray:
    def __init__(self, path_to_words_json=None, path_to_logfile=None, isSpeedrun=False):
        self.path_to_words_json = path_to_words_json
        self.path_to_logfile = path_to_logfile
        self.lock = Lock()
        self.isSpeedrun = isSpeedrun

        # initalize array
        self.botarray = []

    # append the botarray
    def append(self, login: str, passwd: str):
        self.botarray.append(
            Bot(
                login=login,
                passwd=passwd,
                lock=self.lock,
                path_to_words_json=self.path_to_words_json,
                path_to_logfile=self.path_to_logfile,
                isSpeedrun=self.isSpeedrun,
            )
        )

    # start all the sessions simultaneously and wait for them
    def start(self):
        for bot in self.botarray:
            bot.proc = Thread(target=bot.start)
            bot.proc.start()

        for bot in self.botarray:
            bot.proc.join()

    # start all the sessions with different random delay and wait for them
    def start_with_random_delay(self, dmin=0, dmax=60):
        for bot in self.botarray:
            bot.proc = Thread(target=bot.start, kwargs={"delay": randrange(dmin, dmax)})
            bot.proc.start()

        for bot in self.botarray:
            bot.proc.join()
