from contextlib import nullcontext
from datetime import datetime
import json
import requests
from time import sleep, time
import random

from .instaling import Instaling
from .answer import Answer
from .error import BadAnswerError, BadStudentIdUrlError, SessionEnd
from .log import Log

class Bot:
    def __init__(self, 
    login, 
    passwd, 
    lock = nullcontext(), 
    path_to_words_json = None, 
    path_to_logfile = None,
    isSpeedrun = False):
        self.login = login
        self.passwd = passwd
        self.lock = lock
        self.isSpeedrun = isSpeedrun
        self.path_to_words_json = path_to_words_json
        self.path_to_logfile = path_to_logfile
        
        # open logfile and handle
        self.log = Log(
            path_to_logfile= path_to_logfile,
            login= login,
            lock= lock
        )

        # log in
        try:
            self.instaling = Instaling(
                login= self.login,
                passwd= self.passwd
            )
        except BadStudentIdUrlError:
            self.log.bad_student_id_url()
            exit(1)
        
        # open words in json 
        with self.lock:
            try:
                with open(path_to_words_json, "r") as wordsfile:
                    wordsfile_content = wordsfile.readline()
                    if wordsfile_content == "":                          # empty file causes error in json decoding
                        self.words = {}
                    else:
                        try:
                            self.words = json.loads(wordsfile_content)
                        except json.JSONDecodeError:
                            with open(path_to_logfile, "a", encoding="utf-8") as logfile:
                                logfile.write(f"{datetime.now()} Cannot decode json file!\n")
                self.path_to_words_json = path_to_words_json
            except FileNotFoundError:
                with open(path_to_logfile, "a", encoding="utf-8") as logfile:
                    logfile.write(f"{datetime.now()} Lack of json file, creating new one!\n")
                
                self.words = {}
                with open(path_to_words_json, "w", encoding="utf-8") as wordsfile:
                    wordsfile.write(json.dumps(self.words))
                

    # start instaling session
    def start(self):

        # log 
        self.log.session_started()

        #iteracja przez sesje
        while(True):

            # request for next word
            try:
                usage_example = self.instaling.generate_new_word()
            except SessionEnd:
                # log 
                self.log.session_completed()
                break

            # imitate typing... 
            if not self.isSpeedrun:
                sleep(random.randrange(3, 15))

            # check if word is known
            if usage_example in self.words:
                # if known - send it
                answer = self.instaling.send_answer(self.words.get(usage_example))
                if not answer.isCorrect:
                    #log
                    self.log.bad_answer()
                    self.instaling.logout()
                    raise BadAnswerError
            else:
                # if not known - send 💀 and save answer
                answer = self.instaling.send_answer("💀")
                self.words[usage_example] = answer.word

        # zapisz złówka do jsona
        with self.lock:
            with open(self.path_to_words_json, "r") as wordsfile:
                words_to_compare = json.loads(wordsfile.readline())
                for word in words_to_compare:
                    if self.words.get(word) == None:
                        self.words[word] = words_to_compare.get(word)
            with open(self.path_to_words_json, "w") as wordsfile:
                wordsfile.write(json.dumps(self.words))