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
from Translator import Translator
from termcolor import colored, cprint

def main(useShm):

    host1 = "https://translate.google.cn/"
    host2 = "https://translate.google.com/"

    proxy = { "https":"localhost:8123" }

    '''
    加了-s参数后会置1 useShm,
    表示用于取词翻译的内存共享设置
    '''
    if useShm:
        warnings.simplefilter("ignore")
        path = "/tmp"
        projectID = 2333
        key = ipc.ftok(path, projectID)
        shm = ipc.SharedMemory(key, 0, 0)
        shm.attach(0,0)

    tran = Translator( targetLang='zh-CN', host=host1, proxy=None, timeout=1 )

    while True:
        try:
            #获取次数为1则从参数中获取，不用input获取
            if times == 1:
                In = sys.argv[1]
            else:
                In = str(input('>> '))
            if In == '':
                continue

        except:
            print()
            print('Good bye~')
            sys.exit()

        try:
            dataList = tran.getTran(In)
        except Exception as e:
            print(e)
            tran = Translator( targetLang='zh-CN', host=host2, proxy=proxy, timeout=1)
            try:
                dataList = tran.getTran(In)
            except Exception as e:
                print(e)
                '''
                如果只是获取参数的翻译结果，失败后当退出，防止
                一直失败导致无限循环尝试代理连接'''
                if times == 1:
                    sys.exit(1)
                continue

        #有用数据下标 0, 1, 11, 12
        #0: 返回到界面的直接翻译
        #1: 各词性的其他翻译
        #11:不同词性的同义词
        #12:英语解释

        #获取翻译界面的直接结果
        string = str(dataList[0][0][0])
        if useShm:
            shm.write(string+'|', 1)
            offset = len((string+'|').encode('utf8'))
        else:
            cprint('    '+In+' : '+string, 'cyan')

        #英语释义
        if len(dataList) > 12:
            string = tran.getSynonym(dataList[12], 0)
            #排除空字符串
            if string:
                string.replace('\n', '')
                if useShm:
                    string +=  '|'
                    shm.write(string, offset+1)
                    offset = len(string.encode('utf8')) + offset
                else:
                    print()
                    cprint("    英语释义:", 'cyan')
                    for i,ch in enumerate(string):
                        if i % 60 == 0:
                            print()
                            print('      ',end='')

                        cprint(ch, 'cyan', end='')
                    print()

        #其他翻译结果
        string = tran.getMoreTran(dataList[1], dataList[0][0][1])
        if string:
            string.replace('\n', '')
            if useShm:
                string += '|'
                shm.write(string, offset+1)
                offset = len(string.encode('utf8')) + offset
            else:
                '''
                因为此翻译程序用在了其他工程项目，加入了符号'|'用于满足
                其他工程, 这里没有必要使用，因此要将他们消除掉
                '''
                print()

                length = len(string)
                list1 = list(string)
                for i in range(length-1, 0, -1):
                    if list1[i] == '|':
                        list1[i] = '\0'
                        break;

                str1 = ''.join(list1).replace('|', '\n        |-')
                try:
                    index = str.index(str1, '\n')
                    cprint('      '+str1[:index], 'yellow')
                    cprint(str1[index:])
                    print()
                except:
                    pass

        if len(dataList) > 12:
            if dataList[11] is not None:
                string = tran.getSynonym(dataList[11])
                if string:
                    string = "    相关: "+string
                    if useShm:
                        shm.write(string, offset+1)
                        offset = len(string.encode('utf8')) + offset
                    else:
                        #优化显示的需要，让字符串在一行内不要显示的太长
                        if len(string) > 60:
                            cprint(string[:60], 'green')
                            cprint('          '+string[60:], 'green')
                        else:
                            cprint(string, 'green')

        if useShm:
            '''
            用于其他工程项目,在第一字节内写入1表示
            内容写入完毕
            '''
            print(shm.read())
            print(shm.read().decode('utf8'))
            shm.write('1', 0)

        if times == 1:
            print()
            sys.exit(0)

        print()

if __name__ == '__main__':

    #共享内存使用标识
    useShm = 0
    times = 0
    sys.argv.remove(sys.argv[0])
    if len(sys.argv) >= 1:
        for arg in sys.argv:
            if arg == '-s':
                print('Using SharedMemory')
                useShm = 1
            else:
                times = 1
                pass

    main(useShm)
