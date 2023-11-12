import os
from datetime import datetime
import inspect
from colorama import Fore, Back, Style, init

CRITICAL = 50
ERROR = 40
WARN = 30
INFO = 20
DEBUG = 10

_levelToName = {
    CRITICAL: "CRITICAL",
    ERROR: "ERROR",
    WARN: "WARNING",
    INFO: "INFO",
    DEBUG: "DEBUG",
}

_nameToLevel = {
    "CRITICAL": CRITICAL,
    "ERROR": ERROR,
    "WARN": WARN,
    "INFO": INFO,
    "DEBUG": DEBUG,
}

_levelToColor = {
    CRITICAL: Fore.LIGHTRED_EX,
    ERROR: Fore.RED,
    WARN: Fore.YELLOW,
    INFO: Fore.GREEN,
    DEBUG: Fore.BLUE,
}


# print(_levelToColor[CRITICAL] + "'21331123" + Fore.RESET)
# print(_levelToColor[ERROR] + "'21331123" + Fore.RESET)


print(int("-1"))

import time

print(time.strftime("%Y-%m-%d %H:%M:%S"))
