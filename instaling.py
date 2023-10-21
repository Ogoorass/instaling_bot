import requests
import time
import json

if __name__ == "__main__":
    #---queue---
    lista_kont = []
    try:
        with open("lista_kont.txt", "r") as f:
            for line in f:
                lista_kont.append(line.strip('\n').split())
    except FileNotFoundError:
        print("Nie znaleziono pliku z lisą kont!\n")
        exit(1)



    #inicjalizacja sesji
    url = "https://instaling.pl"
    headers = {"connection": "keep-alive"}
    init_request = requests.get(url, headers=headers)
    phpsessionid = init_request.cookies.get("PHPSESSID")
    if phpsessionid == None:
        print("Brak id sesji!")
        exit(1)


    #---iteracja przez queue---
    for konto in lista_kont:
        #logowanie
        url = "https://instaling.pl/teacher.php?page=teacherActions"
        headers = {
            "Referer": "https://instaling.pl/teacher.php?page=login",
            "content-type": "application/x-www-form-urlencoded",
            "cookie": f"PHPSESSID={phpsessionid}; app=app_82;",
            "connection": "keep-alive"
        }
        request_obj = {"action": "login", "from": "", "log_email": konto[0], "log_password": konto[1]}
        cookies = {
            "app": "app_82",
            "PHPSESSID": phpsessionid,
            }

        log_request = requests.post(url, headers=headers, data=request_obj)

        # akutalizuj php session id
        phpsessionid = log_request.history[0].cookies.get("PHPSESSID")
        
        # przykładowy url: "https://instaling.pl/student/pages/mainPage.php?student_id=1245553"
        # jeżeli z jakiegoś powodu będzie inna ilość argumentów to ma pokazać błąd
        student_id = log_request.url.split("?")[-1]
        if("student_id" not in student_id):
            print("Login request error: bad url")
            exit(1)
        student_id = student_id.split("=")[-1]


        #rozpocznij sesje
        url = f"https://instaling.pl/ling2/html_app/app.php?child_id={student_id}"
        
        headers = {
            "connection": "keep-alive",
            "cookie": f"app: app_82; PHPSESSID={phpsessionid}",
            "Referer": f"https://instaling.pl/student/pages/mainPage.php?student_id={student_id}",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "same-origin"
        }

        pre_sessino_request = requests.get(url, headers=headers)

        #iteracja przez sesje
        while (True):
            url = "https://instaling.pl/ling2/server/actions/generate_next_word.php"
            headers = {
                "connection": "keep-alive",
                "cookie": f"app: app_82; PHPSESSID={phpsessionid}",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
            }
            data = {
                "child_id": student_id,
                "date": int(time.time())
            }

            question_request = requests.post(url, headers=headers, data=data)
            
            # wydobywanie pytania i tłumaczenia ze storny
            usage_example = json.loads(question_request.text)['usage_example']
            translation = json.loads(question_request.text)['translations']

            print(usage_example, translation)
            #TODO kwerenda do bazy danych z powyższymi danymi
            #jeżeli rekord znaleziony to go wpisać
            #jezeli rekord nie znaleziony to nic nie wpisywać i przejść dalej, następnie odpowiedź dodać do bazy danych

            exit(0)
        


        
        #---zrób sesję kożystając z bazy dancyh słówek---

