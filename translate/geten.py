#!/usr/bin/python3

import sys
import re
import json
import urllib
from Translator import Translator
from termcolor import colored, cprint

host1 = "https://translate.google.cn/"
host2 = "https://translate.google.com/"

proxy = { "https":"localhost:8123" }
tran = Translator( targetLang='en', host=host1, proxy=None, timeout=1 )


if len(sys.argv) < 2:
    print('Need words')
    sys.exit

for i in range(1, len(sys.argv)):

    try:
        dataList = tran.getTran(sys.argv[i])
        host = host1
    except Exception as e:
        print(e)
        try:
            tran = Translator( targetLang='en', host=host2, proxy=proxy, timeout=1 )
            host = host2
            dataList = tran.getTran(sys.argv[i])
        except Exception as e:
            print(e)
            sys.exit()

    tran.extractData(dataList, host)
