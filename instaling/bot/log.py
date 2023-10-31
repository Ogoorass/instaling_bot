from multiprocessing import Lock
from datetime import datetime

class Log:
    def __init__(self, path_to_logfile, login, lock: Lock):
        self.path_to_logfile = path_to_logfile
        self.lock = lock
        self.login = login

    # log that sesstion has sterted
    def session_started(self):
        with open(self.path_to_logfile, 'a', encoding="utf-8") as logfile, self.lock:
            logfile.write(f"{datetime.now()} Session started for user {self.login}\n")

    # log thet session has endded
    def session_completed(self):
        with open(self.path_to_logfile, 'a') as logfile, self.lock:
            logfile.write(f"{datetime.now()} Session completed for user {self.login}\n")

    def bad_answer(self):
        with open(self.path_to_logfile, 'a') as logfile, self.lock:
            logfile.write(f"{datetime.now()} Bad answer in json for user {self.login}\n")
    
    def bad_student_id_url(self):
        with open(self.path_to_logfile, 'a') as logfile, self.lock:
            logfile.write(f"{datetime.now()} Bad student id url in json for user {self.login}\n")