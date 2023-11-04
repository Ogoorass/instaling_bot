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

        self.words = {}
        


        if path_to_logfile == None:
            # debug loggin config
            logging.basicConfig(
                level=logging.DEBUG, 
                format=f'%(asctime)s - %(levelname)s - {self.login} - %(message)s')
        else:
            # info debug confing
            logging.basicConfig(
                filename=path_to_logfile, 
                level=logging.INFO, 
                format=f'%(asctime)s - %(levelname)s - {self.login} - %(message)s')


        # log in
        try:
            self.instaling = Instaling(
                login= self.login,
                passwd= self.passwd
            )
        except LoginError:
            logging.critical(f"Error when logging in!")
            exit(1)
        
        # open words in json 
        with self.lock:
            try:
                with open(self.path_to_words_json, "r", encoding="utf-8") as wordsfile:
                    try:
                        self.words = json.load(wordsfile)
                        logging.debug(f"json file content: {self.words}")
                    except json.JSONDecodeError:
                        logging.warning("Cannot decode json file, ignoring content!")

            except FileNotFoundError:
                logging.warning(f"No such file \'{self.path_to_words_json}\', ignoring content!")
                
                with open(self.path_to_words_json, "w", encoding="utf-8") as wordsfile:
                    json.dump({}, wordsfile)
                

    # start instaling session
    def start(self, 
        delay=0     # minutes to delay executing the session
    ):

        logging.info(f"delaying {delay} minutes")
        sleep(delay * 60) # minutes to seconds convertion

        # log 
        #self.log.session_started()
        logging.info(f"Session started!")

        #iteracja przez sesje
        while(True):

            # request for next word
            try:
                usage_example = self.instaling.generate_next_word()
                logging.debug(f"usage example: {usage_example}")
            except SessionEnd:
                # log 
                #self.log.session_completed()
                logging.info(f"Session completed!")
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
                    logging.critical(f"Error while sending an answer request")
                    exit(1)
                # if something is messed up raise an error
                if not answer.isCorrect:
                    #log
                    #self.log.bad_answer()
                    logging.warning(f"Bad answer in json")
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
                    logging.critical(f"Error while sending an answer request")
                    exit(1)
                self.words[usage_example] = answer.word

        # zapisz złówka do jsona
        try:
            with open(self.path_to_words_json, "r", encoding="utf-8") as wordsfile, self.lock:
                words_to_compare = json.load(wordsfile)

            for word in words_to_compare:
                if self.words.get(word) == None:
                    logging.debug(f"word {word} not known, adding to json")
                    self.words[word] = words_to_compare.get(word)
        
        except FileNotFoundError:
            logging.warning(f"file {path_to_words_json} deleted during the execution, creating new one")

        except json.JSONDecodeError:
            logging.warning(f"file {path_to_words_json} corruption during the execution, ignoring content and overwriting")

        finally:
            with open(self.path_to_words_json, "w", encoding="utf-8") as wordsfile, self.lock:
                json.dump(self.words, wordsfile)

