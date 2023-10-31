from instaling import Botarray, Account
import os
from sys import platform

def main():

    HOME = os.environ['HOME'] + "/" if platform in ["linux", "linux2"] else ""

    # load accounts from the file
    lista_kont = []
    try:
        with open(f"{HOME}lista_kont.txt", "r") as f:
            for line in f:
                try:
                    login, passwd = line.strip('\n').split()
                except ValueError:
                    print("Błędny format pliku \"lista_kont.txt\"!")
                    exit(1)
                lista_kont.append(Account(login=login, passwd=passwd))
    except FileNotFoundError:
        print("Brak pliku z kontami!")
        exit(1)

    # setup botarray
    lista_botów = Botarray(
        path_to_logfile=f"{HOME}log.txt",
        path_to_words_json=f"{HOME}words.json",
        isSpeedrun= True
    )

    # fill botarray
    for konto in lista_kont:
        lista_botów.append(
            login=konto.login,
            passwd=konto.passwd
        )
    
    # start sessions
    lista_botów.start()


if __name__ == "__main__":
    main()