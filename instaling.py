#!/bin/env python3
import requests
import time
from datetime import datetime
import json

if __name__ == "__main__":

    #otwarcie pliku z logami
    instaling_log_file = open("instaling_log.txt", "a", encoding="utf-8")
    instaling_log_file.write(f"{datetime.now()} Uruchomiono skrypt\n")

    #---queue---
    lista_kont = []
    try:
        with open("lista_kont.txt", "r") as f:
            for line in f:
                lista_kont.append(line.strip('\n').split())
    except FileNotFoundError:
        instaling_log_file.write(f"{datetime.now()} Nie odnaleziono pliku z kontami!\n")
        exit(1)
    
    #załąduj słówka z jsona
    words = {}
    try:
        with open("instaling_words.json", "r") as f:
            words = json.loads(f.readline())
    except FileNotFoundError:
        instaling_log_file.write(f"{datetime.now()} Brak pliku json ze słówkami, tworzenie nowego!\n")
        with open("instaling_words.json", "w") as f:
            f.write(json.dumps(words))

    #---iteracja przez queue---
    for konto in lista_kont:

        instaling_log_file.write(f"{datetime.now()} Sesja rozpoczęta dla użytkownika {konto[0]}\n")

        #inicjalizacja połączenia
        session_instaling = requests.Session()

        url = "https://instaling.pl"
        deafult_headers = { "content-type": "application/x-www-form-urlencoded",
                            "connection": "keep-alive"}
        session_instaling.headers.update(deafult_headers)
        init_request = session_instaling.get(url)
        
        #logowanie
        url = "https://instaling.pl/teacher.php?page=teacherActions"
        login_data = {"action": "login", "from": "", "log_email": konto[0], "log_password": konto[1]}
        login_request = session_instaling.post(url, data=login_data)
        
        # przykładowy url: "https://instaling.pl/student/pages/mainPage.php?student_id=1245553"
        # jeżeli z jakiegoś powodu będzie inna ilość argumentów to ma pokazać błąd
        student_id = login_request.url.split("?")[-1]
        if("student_id" not in student_id):
            instaling_log_file.write(f"{datetime.now()} Błąd requestu login: zły url: {login_request.url}; Użytkownik: {konto[0]}\n")
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
                "date": int(time.time())
            }
            question_request = session_instaling.post(url, data=data)
            
            # wydobywanie pytania i tłumaczenia ze storny
            # jeżeli nie ma tych wartości to znaczy, że sesja zostałą skończona
            try:
                usage_example = json.loads(question_request.text)['usage_example']
                translation = json.loads(question_request.text)['translations']
                word_id = json.loads(question_request.text)['id']
            except KeyError:
                instaling_log_file.write(f"{datetime.now()} Sesja zakończona dla użytkownika {konto[0]}\n")
                break

            url = "https://instaling.pl/ling2/server/actions/save_answer.php"
            data = {
                "child_id": student_id,
                "word_id": word_id,
                "answer": "",
                "version": "C65E24B29F60B1231EC23D979C9707D2"
            }

            #sprawdź czy jest już w dictcie words
            if(words.get(usage_example)):
                #jeżeli jest to go podaj
                data["answer"] = words.get(usage_example)
                save_answer_request = session_instaling.post(url, data=data)
            else:
                #jezeli nie ma to przejdź dalej i wpisz do dicta
                save_answer_request = session_instaling.post(url, data=data)
                words[usage_example] = json.loads(save_answer_request.text)['word']
        
        # wyloguj się
        url = "https://instaling.pl/teacher2/logout.php"
        logout_request = requests.get(url)


    #zapisz słówka do jsona
    with open("instaling_words.json", "w") as f:
        f.write(json.dumps(words))

    instaling_log_file.write(f"{datetime.now()} Zakończono pomyślnie\n")
    instaling_log_file.close()