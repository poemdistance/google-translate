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

    tran = Translator(
            targetLang='zh-CN',
            host="https://translate.google.cn/",
            proxy=None,
            timeout=2,
            )

    while True:
        try:
            #基目录为家目录,pic2char参数为home下的文件夹
            data = tran.pic2char("Pictures/pic/")
        except Exception as e:
            print('Exception: ', e)
            sys.exit()

        #data = data.replace('\n', ' ')
        cprint(data, 'yellow')

        dataList = tran.getTran(data);
        length = len(dataList[0])
        for i in range(length-1):
            cprint('    ---> '+dataList[0][i][0], 'cyan')
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
