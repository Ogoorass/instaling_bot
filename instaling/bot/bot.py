from contextlib import nullcontext
from datetime import datetime
import json
import requests
from time import sleep, time
import random
import logging

from .instaling import Instaling
from .answer import Answer
from .error import BadAnswerError, SessionEnd, SendAnswerError, LoginError
from .log import Log

class Bot:
    def __init__(self, 
    login, 
    passwd, 
    lock = nullcontext(), 
    path_to_words_json = "words.json", 
    path_to_logfile = None,
    isSpeedrun = False):
        self.login = login
        self.passwd = passwd
        self.lock = lock
        self.isSpeedrun = isSpeedrun
        self.path_to_words_json = path_to_words_json
        self.path_to_logfile = path_to_logfile
        


        if path_to_logfile == None:
            # debug loggin config
            logging.basicConfig(
                level=logging.DEBUG, 
                format='%(asctime)s - %(levelname)s - %(message)s')
        else:
            # info debug confing
            logging.basicConfig(
                filename=path_to_logfile, 
                level=logging.INFO, 
                format='%(asctime)s - %(levelname)s - %(message)s')



        # log in
        try:
            self.instaling = Instaling(
                login= self.login,
                passwd= self.passwd
            )
        except LoginError:
            logging.critical(f"Error when logging in as {self.login}")
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
                            logging.warning("Cannot decode json file, ignoring content!")

                self.path_to_words_json = path_to_words_json
            except FileNotFoundError:
                logging.warning("Lack of json file, creating new one!")
                
                self.words = {}
                with open(path_to_words_json, "w", encoding="utf-8") as wordsfile:
                    wordsfile.write(json.dumps(self.words))
                

    # start instaling session
    def start(self):

        # log 
        #self.log.session_started()
        logging.info(f"Session started for user {self.login}")

        #iteracja przez sesje
        while(True):

            # request for next word
            try:
                usage_example = self.instaling.generate_new_word()
                logging.debug(f"usage example: {usage_example}")
            except SessionEnd:
                # log 
                #self.log.session_completed()
                logging.info(f"Session completed for user {self.login}")
                self.instaling.logout()
                break

            # imitate typing... 
            if not self.isSpeedrun:
                time_typing_imaginary = random.randrange(3, 15)
                logging.debug(f"Typing (waiting) for {time_typing_imaginary} seconds")
                sleep(time_typing_imaginary)

            # check if word is known
            if usage_example in self.words:

                logging.debug(f"usage example is known, answer - \'{self.words.get(usage_example)}\'")
                # if known - send it
                try:
                    answer = self.instaling.send_answer(self.words.get(usage_example))
                except SendAnswerError:
                    # exit if something is wrong
                    #self.log.send_answer_error()
                    logging.critical(f"Error while sending an answer request for user {self.login}")
                    exit(1)
                # if something is messed up raise an error
                if not answer.isCorrect:
                    #log
                    #self.log.bad_answer()
                    logging.warning(f"Bad answer in json for user {self.login}")
                    raise BadAnswerError
            else:

                logging.debug("usage example is not known")
                # if not known - send 💀 and save answer
                try:
                    answer = self.instaling.send_answer("💀")
                    logging.debug(f"the answer is \'{answer.word}\'")
                except SendAnswerError:
                    # exit if something is wrong
                    #self.log.send_answer_error()
                    logging.critical(f"Error while sending an answer request for user {self.login}")
                    exit(1)
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