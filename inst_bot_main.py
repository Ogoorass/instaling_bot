from instaling import Bot, Lock_bot

class Konto:
    def __init__(self, login, passwd):
        self.login = login
        self.passwd = passwd

if __name__ == "__main__":

    # załaduj konta z pliku
    lista_kont = []
    try:
        with open("lista_kont.txt", "r") as f:
            for line in f:
                login, passwd = line.strip('\n').split()
                lista_kont.append(Konto(login=login, passwd=passwd))
    except FileNotFoundError:
        print("Brak pliku z kontami!")
        exit(1)

    lock = Lock_bot()

    lista_botów = []
    for konto in lista_kont:
        lista_botów.append(Bot(
            login=konto.login,
            passwd=konto.passwd,
            lock=lock,
            path_to_words_json= "instaling_words.json",
            path_to_logfile= "instaling_log.txt",
        ))

    for bot in lista_botów:
        bot.start_subprocess()

    for bot in lista_botów:
        bot.join_subprocess()
    