#!/usr/bin/python3

import sys
import re
import json
import urllib
import readline
from langdetect import detect
from Translator import Translator
from termcolor import colored, cprint

def main():

    host1 = "https://translate.google.cn/"
    host2 = "https://translate.google.com/"

    proxy = { "https":"localhost:8123" }

    tran = Translator( targetLang='en', host=host1, proxy=None, timeout=1 )

    while True:
        try:
            In = str(input('>> '))
            if In == '':
                print()
                continue

        except:
            print()
            print('Good bye~')
            sys.exit()

        try:
            dataList = tran.getTran(In)
        except Exception as e:
            print(e)
            tran = Translator( targetLang='en', host=host2, proxy=proxy, timeout=1)
            try:
                dataList = tran.getTran(In)
            except Exception as e:
                print(e)
                continue

        #有用数据下标 0, 1, 11, 12
        #0: 返回到界面的直接翻译
        #1: 各词性的其他翻译
        #11:不同词性的同义词
        #12:英语解释
        
        cprint('    ---> '+dataList[0][0][0], 'cyan')

        if len(dataList) > 12:
            cprint('    ', end='')
            tran.getSynonym(dataList[12], 0)

        tran.getMoreTran(dataList[1])

        if len(dataList) > 12:
            if dataList[11] is not None:
                print()
                cprint('    同义词: ', 'yellow',  end='')
                tran.getSynonym(dataList[11])

if __name__ == '__main__':
    main()
