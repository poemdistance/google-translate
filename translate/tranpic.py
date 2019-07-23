#!/usr/bin/python3

import os
import sys
import readline
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
            print('Waiting...')
            data = tran.pic2char("Pictures/pic/")
        except Exception as e:
            print('Exception: ', e)
            sys.exit()


        data = data.replace('\n', ' ')
        if not data.isspace() and not len(data)==0:
            cprint(data, 'yellow')
        else:
            print('No string found')
            print('Wait for another...')
            continue

        os.system('/usr/bin/tranen '+data)

if __name__ == '__main__':
    main()
