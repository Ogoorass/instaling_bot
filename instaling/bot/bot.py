from contextlib import nullcontext
from .session import session
from datetime import datetime
import json

class Bot:
    def __init__(self, 
    login, 
    passwd, 
    lock = nullcontext(), 
    path_to_words_json = None, 
    path_to_logfile = None,
    speedrun = False):
        self.login = login
        self.passwd = passwd
        self.lock = lock
        self.speedrun = speedrun
        
        # open logfile
        with self.lock:
            try:
                f = open(path_to_logfile, "a", encoding="utf-8")
            except FileNotFoundError:
                print("Błędna ścieżka pliku z logami!\n")
                exit(1)
            else:
                f.close()
                self.path_to_logfile = path_to_logfile
        
        # open words in json 
        with self.lock:
            try:
                with open(path_to_words_json, "r") as wordsfile:
                    wordsfile_content = wordsfile.readline()
                    if wordsfile_content == "":                                # empty file causes error in json decoding
                        self.words = {}
                    else:
                        try:
                            self.words = json.loads(wordsfile_content)
                        except json.JSONDecodeError:
                            with open(path_to_logfile, "a", encoding="utf-8") as logfile:
                                logfile.write(f"{datetime.now()} Nie można dekodować pliku json\n")
                self.path_to_words_json = path_to_words_json
            except FileNotFoundError:
                with open(path_to_logfile, "a", encoding="utf-8") as logfile:
                    logfile.write(f"{datetime.now()} Brak pliku json ze słówkami, praca bez pliku!\n")
                self.words = {}

    # start instaling session
    def start(self):
        session(self)