class Url:
    init = "https://instaling.pl"
    login = "https://instaling.pl/teacher.php?page=teacherActions"
    next_word = "https://instaling.pl/ling2/server/actions/generate_next_word.php"
    answer = "https://instaling.pl/ling2/server/actions/save_answer.php"
    logout = "https://instaling.pl/teacher2/logout.php"


class Header:
    default = {
        "content-type": "application/x-www-form-urlencoded",
        "connection": "keep-alive",
    }


class Data:
    def login(login, passwd):
        return {
            "action": "login",
            "from": "",
            "log_email": login,
            "log_password": passwd,
        }

    def next_word(student_id, time):
        return {"child_id": student_id, "date": time}

    def answer(answer, student_id, word_id):
        return {
            "child_id": student_id,
            "word_id": word_id,
            "answer": answer,
            "version": "C65E24B29F60B1231EC23D979C9707D2",
        }
