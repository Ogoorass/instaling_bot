from instaling import Botarray, Account
import os
from sys import platform


def main():

    # for different systems
    HOME = os.environ["HOME"] + "/" if platform in ["linux", "linux2"] else ""

    # load accounts from the file
    accounts = []
    try:
        with open(f"{HOME}accounts.txt", "r") as f:
            for line in f:
                try:
                    login, passwd = line.strip("\n").split()
                except ValueError:
                    print('Bad format of "accounts.txt"!')
                    exit(1)
                accounts.append(Account(login=login, passwd=passwd))
    except FileNotFoundError:
        print("Lack of account file!")
        exit(1)

    # setup botarray
    botarray = Botarray(
        path_to_logfile=f"{HOME}log.txt", path_to_words_json=f"{HOME}words.json"
    )

    # fill botarray
    for account in accounts:
        botarray.append(login=account.login, passwd=account.passwd)

    # start sessions
    botarray.start_with_random_delay()


if __name__ == "__main__":
    main()
