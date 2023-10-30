import requests
from time import sleep, time
from datetime import datetime
import json
import random


# wykonuje sesję instalinga
def session(self):
    #inicjalizacja połączenia
    session_instaling = requests.Session()
    url = "https://instaling.pl"
    deafult_headers = { "content-type": "application/x-www-form-urlencoded",
                        "connection": "keep-alive"}
    session_instaling.headers.update(deafult_headers)
    init_request = session_instaling.get(url)
    # log
    with open(self.path_to_logfile, "a", encoding="utf-8") as logfile, self.lock:
        logfile.write(f"{datetime.now()} Sesja rozpoczęta dla użytkownika {self.login}\n")
    
    #logowanie
    url = "https://instaling.pl/teacher.php?page=teacherActions"
    login_data = {"action": "login", "from": "", "log_email": self.login, "log_password": self.passwd}
    login_request = session_instaling.post(url, data=login_data)
    # przykładowy url: "https://instaling.pl/student/pages/mainPage.php?student_id=1245553"
    # jeżeli z jakiegoś powodu będzie inna ilość argumentów to ma pokazać błąd
    student_id = login_request.url.split("?")[-1]
    if "student_id" not in student_id:
        # log
        with open(self.path_to_logfile, "a", encoding="utf-8") as logfile, self.lock:
            logfile.write(f"{datetime.now()} Błąd requestu login: zły url: {login_request.url}; Użytkownik: {self.login}\n")
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
            with open(self.path_to_logfile, "a", encoding="utf-8") as logfile, self.lock:
                logfile.write(f"{datetime.now()} Sesja zakończona dla użytkownika {self.login}\n")
            break
        url = "https://instaling.pl/ling2/server/actions/save_answer.php"
        data = {
            "child_id": student_id,
            "word_id": word_id,
            "answer": "💀",
            "version": "C65E24B29F60B1231EC23D979C9707D2"
        }
        if not self.speedrun:
            sleep(random.randrange(3, 15))
        #sprawdź czy jest już w dictcie words
        if self.words.get(usage_example):
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
    with self.lock:
        with open(self.path_to_words_json, "r") as wordsfile:
            words_to_compare = json.loads(wordsfile.readline())
            for word in words_to_compare:
                if self.words.get(word) == None:
                    self.words[word] = words_to_compare.get(word)
        with open(self.path_to_words_json, "w") as wordsfile:
            wordsfile.write(json.dumps(self.words))