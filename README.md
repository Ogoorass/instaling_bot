# instaling_bot
Automatically run Instaling

## Simple usage

To run Instaling session just make a `Bot` object and provide `login` and `password`, then call the `start()` method.

```python
from instaling import Bot

Bot(login="xx213769", passwd="jp2gmd").start()
```

If not provided `path_to_words_json` it creates in run direcory file `words.json`, where it stores all the words used in sesson for further usage. Similarly the `path_to_logfile` if not provided it creates `log.txt`, where will be all logs.

## More complex usage

Example of more complex usage is in `main.py` file in root direcory.

```python
from instaling import Botarray, Account
import os
from sys import platform

def main():

    HOME = os.environ['HOME'] + "/" if platform in ["linux", "linux2"] else ""

    # load accounts from the file
    accounts = []
    try:
        with open(f"{HOME}accounts.txt", "r") as f:
            for line in f:
                try:
                    login, passwd = line.strip('\n').split()
                except ValueError:
                    print("Bad format of \"accounts.txt\"!")
                    exit(1)
                accounts.append(Account(login=login, passwd=passwd))
    except FileNotFoundError:
        print("Lack of account file!")
        exit(1)

    # setup botarray
    botarray = Botarray(
        path_to_logfile=f"{HOME}log.txt",
        path_to_words_json=f"{HOME}words.json",
        isSpeedrun= True
    )

    # fill botarray
    for account in accounts:
        botarray.append(
            login=account.login,
            passwd=account.passwd
        )
    
    # start sessions
    botarray.start()


if __name__ == "__main__":
    main()
```

The `Botarray` class is made to easly create multiple Instaling sessions.

For initialisation you can provide `path_to_logfile` and `path_to_words_json`. Then by calling the `append()` method and specifying `login` and `password` you can add another accounts to the array. Finally by calling the `start()` method all the elements of the botarray are simultaneously run and waited for. 

The `Account` class is for convenience. 
```python
class Account:
    def __init__(self, login, passwd):
        self.login = login
        self.passwd = passwd
```


