#!/usr/bin/python3

import sys
import re
import json
import urllib
from langdetect import detect
from Translator import Translator
from termcolor import colored, cprint

def getMoreTran(data):

    try:
        print()
        cprint('    ' + data[0][0] + ': ' + str(data[0][1]), 'yellow')
        print()
        data = data[0][2:]
        for word in data[0]:
            cprint('    ' + word[0] + ': ' + str(word[1]), 'yellow')
    except TypeError:
        pass

def getSynonym(data, flag=1):

    try:
        #cprint('    ' + data[0][0] + ': ' + str(data[0][1][0][0]), 'yellow')
        for i,element in enumerate(data[0][1][0][0]):
            if flag and i > 8:
                break;

            if flag:
                cprint(element, 'yellow', end=', ')
            else:
                cprint(element, 'yellow', end='')

        print()

    except TypeError:
        pass


def main():
    tranen = Translator( targetLang='zh-CN' )
    tranzh = Translator( targetLang='zh-CN' )


    while True:
        cprint('>> ', 'green', end='')
        try:
            In = str(input())
            if In == '':
                continue

            lang = detect(In)
            print('lang = ', lang)
            if lang == 'zh-cn':
                tran = tranen
            else:
                tran = tranzh
        except:
            print()
            print('Good bye~')
            sys.exit()

        dataList = tran.getTran(In)


        #有用数据下标 0, 1, 11, 12
        #0: 返回到界面的直接翻译
        #1: 各词性的其他翻译
        #11:不同词性的同义词
        #12:英语解释
        
        cprint('    '+dataList[0][0][0], 'yellow')

        if len(dataList) > 12:
            cprint('    ', end='')
            getSynonym(dataList[12], 0)

        print()
        cprint('    URL: ' + 'https://translate.google.cn/#view' +
                '=home&op=translate&sl=en&tl=zh-CN&text=' + urllib.request.quote(In), 'green')

        getMoreTran(dataList[1])

        if len(dataList) > 12:
            if dataList[11] is not None:
                print()
                cprint('    同义词: ', 'yellow',  end='')
                getSynonym(dataList[11])

if __name__ == '__main__':
    main()
