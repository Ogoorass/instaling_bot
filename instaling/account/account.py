class Account:
    def __init__(self, login, passwd):
        self.login = login
        self.passwd = passwd

    def __str__(self):
        return f"login= {self.login}\npasswd= {self.passwd}\n"
