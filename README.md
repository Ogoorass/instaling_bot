# instaling_bot
Automatically run Instaling

## Simple usage

To run Instaling session just make a `Bot` object and provide `login` and `password`, then call the `start()` method.

```python
from instaling import Bot

Bot(login="xx213769", passwd="jp2gmd").start()
```

If not provided `path_to_words_json` creates in run direcory file `words.json`, where it stores all the words used in sesson for further usage. Similarly the `path_to_logfile` if not provided creates `log.txt`, where are all logs.


