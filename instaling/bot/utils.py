from .error import BadStudentIdUrlError

# przykładowy url: "https://instaling.pl/student/pages/mainPage.php?student_id=1245553"
# jeżeli z jakiegoś powodu będzie inna ilość argumentów to ma pokazać błąd
def extract_student_id_from_url(url) -> str:
    student_id = url.split("?")[-1]
    if "student_id" not in student_id:
        # log TODO
        # with open(self.path_to_logfile, "a", encoding="utf-8") as logfile, self.lock:
        #    logfile.write(f"{datetime.now()} Błąd requestu login: zły url: {login_request.url}; Użytkownik: {self.login}\n")
        raise BadStudentIdUrlError
    student_id = student_id.split("=")[-1]
    return student_id
