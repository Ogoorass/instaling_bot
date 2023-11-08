# instaling_bot
Python library for automatically running Instaling sessions, made with `requests` module.

## Simple usage

To run an Instaling session, simply create a `Bot` instance, provide `login` and `passwd`, then call the `start` method.

```python
from instaling import Bot

Bot(login="xx213769", passwd="jp2gmd").start()
```

By default, it creates a `words.json` file in the run directory, where it stores all the words used in the session for further usage. This can be overriden using the `path_to_words_json` argument in the `Bot` constructor.
If the `path_to_logfile` argument is not provided, all debug logs are printed to stdout.

By default it imitates typing - waits a few seconds before sending an answer, but you can turn it off with the `isSpeedrun` argument.
```python
bot = Bot(login="xx213769", passwd="jp2gmd", isSpeedrun=True)
```

The `start` method accepts a `delay` argument. This is an optional time in minutes the bot will wait before starting the session. Useful for further human imitation when automating.
```python
bot.start(delay=13)
```

## More complex usage

Example of more complex usage is in `main.py` file in the root direcory.

https://github.com/Ogoorass/instaling_bot/blob/main/main.py

The `Botarray` class is used to easily run Instaling sessions in bulk.

Same as in `Bot`, `path_to_words_json`, `path_to_logfile` and `isSpeedrun` may be provided to the `Botarray` constructor. The `append` method is used to add user accounts to the array. By calling the `start_with_random_delay` method, all elements of the botarray are simultaneously run and waited for, but each of them starts executing with a random delay. By default it is 0 to 60 minutes, but you can specify `dmin` and `dmax`.

```python
from instaling.botarray import Botarray

botarray = Botarray(isSpeedrun=True)

# add accounts
botarray.append(login="xx213769", passwd="jp2gmd")
...
botarray.append(login="xx696969", passwd="czacha")

# start sessions
botarray.start_with_random_delay(dmin=6, dmax=9)
```

If you want to start all sessions at the same time, you can call the plain `start` method.
```python
botarray.start()
```

An `Account` class is provided for convenience. 
```python
class Account:
    def __init__(self, login, passwd):
        self.login = login
        self.passwd = passwd
```
