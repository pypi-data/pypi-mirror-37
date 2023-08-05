py_pushover_simple
==================

[![PyPI version](https://badge.fury.io/py/py-pushover-simple.svg)](https://badge.fury.io/py/py-pushover-simple)

This is a very simple python pushover wrapper for sending quick messages from command line scripts.

## Installation Instructions

1. Download from PyPi:
    
    ```
    python3 -m pip install py_pushover_simple
    ```

2. Add it to your script:

    ```python
    from py_pushover_simple import pushover

    def send_message(message):
        p = pushover.Pushover()
        p.user = 'user_key'
        p.token = 'app_token'

        p.sendMessage(message)
    ```

    For a working demo, see [ippush.py][0]

[0]: https://code.jrgnsn.net/matthew/ip_push/src/branch/master/ippush.py

## Debugging

`py_pushover_simple` has some simple debugging features:

For a full list of arguments:

```
$ python -m py_suchover_simple.pushover -h
usage: pushover.py [-h] [-u <string>] [-t <string>]

optional arguments:
  -h, --help   show this help message and exit
  -u <string>  pushover user token
  -t <string>  pushover app token
```

## Contributors:

- Matthew Jorgensen

## License

This project is licensed inder the terms of the MIT license.