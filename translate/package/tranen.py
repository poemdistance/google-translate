#!/usr/bin/python3

import sys
import re
import json
import select
import urllib
import readline
import warnings
import sysv_ipc as ipc
from langdetect import detect
from translate.package.Translator import Translator
from termcolor import colored, cprint

def main():

    host1 = "https://translate.google.cn/"
    host2 = "https://translate.google.com/"

    proxy = { "https":"localhost:8123" }

    warnings.simplefilter("ignore")

    path = "/tmp"
    projectID = 2333
    key = ipc.ftok(path, projectID)
    
    shm = ipc.SharedMemory(key, 0, 0)
    shm.attach(0,0)

    tran = Translator( targetLang='zh-CN', host=host1, proxy=None, timeout=2 )

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
            tran = Translator( targetLang='zh-CN', host=host2, proxy=proxy, timeout=2)
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
        
        string = str(dataList[0][0][0])+"|"
        shm.write(string, 1)
        offset = len(string.encode('utf8'))

        #英语释义
        if len(dataList) > 12:
            string = tran.getSynonym(dataList[12], 0)
            if string:
                string.replace('\n', '')
                string +=  '|'
                shm.write(string, offset+1)
                offset = len(string.encode('utf8')) + offset
                print("英语释义:", string)
                print("长度:",offset)

        string = tran.getMoreTran(dataList[1], dataList[0][0][1])
        print('词性:', string)
        if string:
            string.replace('\n', '')
            string += '|'
            shm.write(string, offset+1)
            offset = len(string.encode('utf8')) + offset

        if len(dataList) > 12:
            if dataList[11] is not None:
                string.replace('\n', '')
                string = tran.getSynonym(dataList[11])
                if string:
                    string = "同义词:"+string
                    shm.write(string, offset+1)
                    offset = len(string.encode('utf8')) + offset
                    print(string)

        print(shm.read())
        print(shm.read().decode('utf8'))
        shm.write('1', 0)

if __name__ == '__main__':
    main()
