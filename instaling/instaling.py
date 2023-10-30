#!/bin/env python3
import requests
from time import sleep, time
from datetime import datetime
import json
from multiprocessing import Process, Lock
import random

def Lock_bot() -> Lock:
    return Lock()

class Bot:
    def __init__(self, 
    login, 
    passwd, 
    lock: 
    Lock = None, 
    path_to_words_json = None, 
    path_to_logfile = None,
    speedrun = False):
        self.login = login
        self.passwd = passwd
        self.lock = lock
        self.speedrun = speedrun
        
        # open logfile
        try:
            f = open(path_to_logfile, "r", encoding="utf-8")
        except FileNotFoundError:
            print("Błędna ścieżka pliku z logami!\n")
            exit(1)
        else:
            f.close()
            self.path_to_logfile = path_to_logfile

        # open words in json file
        try:
            with open(path_to_words_json, "r") as wordsfile:
                wordsfile_content = wordsfile.readline()
                if(wordsfile_content == ""):                                # empty file causes error in json decoding
                    self.words = {}
                else:
                    try:
                        self.words = json.loads(wordsfile_content)
                    except json.JSONDecodeError:
                        lock.acquire()
                        with open(path_to_logfile, "a", encoding="utf-8") as logfile:
                            logfile.write(f"{datetime.now()} Nie można dekodować pliku json\n")
                        lock.release()
            self.path_to_words_json = path_to_words_json
        except FileNotFoundError:
            lock.acquire()
            with open(path_to_logfile, "a", encoding="utf-8") as logfile:
                logfile.write(f"{datetime.now()} Brak pliku json ze słówkami, praca bez pliku!\n")
            lock.release()
            self.words = {}
                

    # wykonuje sesję instalinga
    def instaling_bot(self):
        #inicjalizacja połączenia
        session_instaling = requests.Session()
        url = "https://instaling.pl"
        deafult_headers = { "content-type": "application/x-www-form-urlencoded",
                            "connection": "keep-alive"}
        session_instaling.headers.update(deafult_headers)
        init_request = session_instaling.get(url)

        # log
        self.lock.acquire()
        with open(self.path_to_logfile, "a", encoding="utf-8") as logfile:
            logfile.write(f"{datetime.now()} Sesja rozpoczęta dla użytkownika {self.login}\n")
        self.lock.release()

        #logowanie
        url = "https://instaling.pl/teacher.php?page=teacherActions"
        login_data = {"action": "login", "from": "", "log_email": self.login, "log_password": self.passwd}
        login_request = session_instaling.post(url, data=login_data)

        # przykładowy url: "https://instaling.pl/student/pages/mainPage.php?student_id=1245553"
        # jeżeli z jakiegoś powodu będzie inna ilość argumentów to ma pokazać błąd
        student_id = login_request.url.split("?")[-1]
        if("student_id" not in student_id):
            # log
            self.lock.acquire()
            with open(self.path_to_logfile, "a", encoding="utf-8") as logfile:
                logfile.write(f"{datetime.now()} Błąd requestu login: zły url: {login_request.url}; Użytkownik: {self.login}\n")
            self.lock.release()
            exit(1)
        student_id = student_id.split("=")[-1]
        #rozpocznij sesje
        url = f"https://instaling.pl/ling2/html_app/app.php?child_id={student_id}"
        pre_sessino_request = session_instaling.get(url)

        #iteracja przez sesje
        while(True):
            #request o kolejne słówko, użwany także do zakończenia sesji
            url = "https://instaling.pl/ling2/server/actions/generate_next_word.php"
            data = {
                "child_id": student_id,
                "date": int(time())
            }
            question_request = session_instaling.post(url, data=data)

            # wydobywanie pytania i tłumaczenia ze storny
            # jeżeli nie ma tych wartości to znaczy, że sesja została skończona
            try:
                usage_example = json.loads(question_request.text)['usage_example']
                word_id = json.loads(question_request.text)['id']
            except KeyError:
                self.lock.acquire()
                with open(self.path_to_logfile, "a", encoding="utf-8") as logfile:
                    logfile.write(f"{datetime.now()} Sesja zakończona dla użytkownika {self.login}\n")
                self.lock.release()
                break
            url = "https://instaling.pl/ling2/server/actions/save_answer.php"
            data = {
                "child_id": student_id,
                "word_id": word_id,
                "answer": "",
                "version": "C65E24B29F60B1231EC23D979C9707D2"
            }

            if(not self.speedrun):
                sleep(random.randrange(3, 15))

            #sprawdź czy jest już w dictcie words
            if(self.words.get(usage_example)):
                #jeżeli jest to go podaj
                data["answer"] = self.words.get(usage_example)
                save_answer_request = session_instaling.post(url, data=data)
            else:
                #jezeli nie ma to przejdź dalej i wpisz do dicta
                save_answer_request = session_instaling.post(url, data=data)
                self.words[usage_example] = json.loads(save_answer_request.text)['word']

        # wyloguj się
        url = "https://instaling.pl/teacher2/logout.php"
        logout_request = session_instaling.get(url)

        # zapisz złówka do jsona
        self.lock.acquire()
        with open(self.path_to_words_json, "r") as wordsfile:
            words_to_compare = json.loads(wordsfile.readline())
            for word in words_to_compare:
                if(self.words.get(word) == None):
                    self.words[word] = words_to_compare.get(word)

        with open(self.path_to_words_json, "w") as wordsfile:
            wordsfile.write(json.dumps(self.words))
        self.lock.release()

    def start_subprocess(self, minutes_to_wait = False):
        if(minutes_to_wait):
            sleep(random.randrange(minutes_to_wait))
        self.process = Process(target=self.instaling_bot)
        self.process.start()
    
    def join_subprocess(self):
        self.process.join()