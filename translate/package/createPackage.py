#!/usr/bin/python3

import sys
import os

#修改导包语句并写入package文件内
def changeNormal(files, dire, flag):
    with open(files, 'r') as f:
        buf = f.read()
        buf = str(buf)
        if flag == 1:
            buf = buf.replace('from Translator ', 
                    'from translate.package.Translator ')
        else:
            buf = buf.replace('from getTK ',
                    'from translate.package.getTK ')

        src = files.split('/')
        src = src[len(src)-1]
        dst = os.path.join(dire, 'package')
        dst = os.path.join(dst, src)
        print('Change and cp src file to: ',dst)
        with open(dst, 'w') as f:
            f.write(buf)

        os.system('chmod +x %s' % (dst))

#直接复制源文件到目标文件
def justCopy(files, dire):
    src = os.path.split(files)
    dst = os.path.join(dire, 'package')
    dst = os.path.join(dst, src[len(src)-1])
    print('cp file to ',dst)
    os.system('cp %s %s -p' % (files, dst))

#对不同文件进行不同的复制操作
def copy(dire, exclude):
    normal1 = ['geten.py', 'getzh.py', 'tranen.py', 'tranzh.py']
    normal2 = ['Translator.py']
    entries = os.listdir(dire)
    for element in entries:
        if not os.path.isdir(os.path.join(dire, element)):
            if element not in exclude:
                if element in normal1:
                    changeNormal(os.path.join(dire, element), dire, 1)
                elif element in normal2:
                    changeNormal(os.path.join(dire, element), dire, 2)
                else:
                    justCopy(os.path.join(dire, element), dire)

if __name__ == '__main__':
    exclude = ['__pycache__', 'package']
    copy(os.path.abspath('translate/'), exclude)

