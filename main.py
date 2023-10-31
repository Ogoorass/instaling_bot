from instaling import Botarray, Account
import os

def main():
    # załaduj konta z pliku
    lista_kont = []
    try:
        with open("lista_kont.txt", "r") as f:
            for line in f:
                login, passwd = line.strip('\n').split()
                lista_kont.append(Account(login=login, passwd=passwd))
    except FileNotFoundError:
        print("Brak pliku z kontami!")
        exit(1)

    HOME = os.environ['HOME']

    lista_botów = Botarray(
        path_to_logfile=f"{HOME}/log.txt",
        path_to_words_json=f"{HOME}/instaling_words.json"
    )

    for konto in lista_kont:
        lista_botów.append(
            login=konto.login,
            passwd=konto.passwd
        )
    
    lista_botów.start()












if __name__ == "__main__":
    main()