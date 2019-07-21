#-*-Coding:utf-8-*-
import os
import sys
import time
import gzip
import json
import urllib
import requests
import pytesseract
from termcolor import colored, cprint
from socket import timeout
from translate.package.getTK import TokenAcquirer
from PIL import Image, PILLOW_VERSION

class Translator(object):

    def __init__(self, targetLang='zh-CN', \
            proxy=None, timeout=3, \
            host='https://translate.google.cn'):

        self.acquire = None;
        self.host = host
        self.targetLang = targetLang
        self.proxy = proxy
        self.session = requests.Session()
        self.timeout = timeout

    def getcookie(self):
        cookie = {
                'cookie':'182=AX2oNMyUeRd8RJ\
                        XqRNGS617RPfUuMCNowbg\
                        BE2A688Le5wzwjkV1sudM\
                        HSW0xyEqe9TKPfeit7fAo\
                        F6vwthqpX7NToId4xhiP_\
                        J0QQi3wasA44rD8rGLMA3\
                        _DQcvrtmJyXh0enZS9bFP\
                        8BBxC1vtQDah39bL1ZbuNL\
                        hJ9CH2yQQ'
                        }
        return cookie

    def getParams(self, word, token ):

        key = []
        val = []

        if self.targetLang == 'en':
            key = ['client','sl','tl','hl','dt',\
                    'dt','dt','dt','dt','dt','dt',\
                    'dt','dt','dt','dt','otf','pc',\
                    'ssel','tsel','kc','tk','q']

            val=['webapp','zh-CN','en','en','at',\
                    'bd','ex','ld','md', 'qca',\
                    'rw','rm','ss','t','gt','1',\
                    '1','3','5','2',token,word]

        elif self.targetLang == 'zh-CN':
            key = ['client','sl','tl','hl','dt',\
                    'dt','dt','dt','dt','dt','dt',\
                    'dt','dt','dt','swap','otf',\
                    'pc','ssel','tsel','kc','tk','q']

            val=['webapp','en','zh-CN','en','at',\
                    'bd','ex','ld','md','qca','rw',\
                    'rm','ss','t','1','1','1','5',\
                    '5','2',token,word]
        else:
            print('Not support target language:\
                    %s yet' % self.targetLang)

        result = ''

        for i in range(len(key)-1):
            result += key[i] + '=' + val[i] + '&'

        result += key[len(key)-1]+ '=' \
                + urllib.parse.quote_plus(word)

        return 'translate_a/single?' + result

    def getHeaders(self):
        headers = {
                'Host': 'translate.google.cn',
                'method': 'GET',
                'scheme': 'https',
                'accept': '*/*',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.5',
                'dnt': '1',
                'referer': self.host,
                'Connection': 'keep-alive',
                'user-agent': 'Mozilla/5.0 (X11; Linux\
                        x86_64) AppleWebKit/537.36 (KH\
                        TML, like Gecko) Chrome/74.0.3\
                        729.108 Safari/537.36',
                        }
        return headers

    def ScanNewFile(self, dirname):
        inTime = time.time()
        home = os.path.expanduser('~/')
        dirname = dirname
        absDir = home + dirname
        num = 0
        print('Wait...', end='')
        try:
            while True:
                time.sleep(1);
                with os.scandir(absDir) as entries:
                    for entry in entries :
                        if entry.is_file():
                            attrs = entry.stat()
                            if attrs.st_mtime > inTime:
                                print('\nFound new file, ', end='')
                                return absDir+entry.name

        except FileNotFoundError as err:
            print(str(err))
            ScanNewFile()
        except KeyboardInterrupt as e:
            print(e)
            sys.exit()

    def ExtractText(self, fileName):
        print('Open image.');
        image = Image.open(fileName)
        text = pytesseract.image_to_string(image)

        return text

    def PrintTran(self, tran):
        print(tran)

    def WaitForFileSavedSuccessfully(self):
        time.sleep(0.2)

    def getTran(self, text):

        baseURL = self.host

        if not self.acquire:
            self.acquire = TokenAcquirer(session=self.session,\
                    proxy=self.proxy, timeout=self.timeout, host=self.host)

            self.tk = self.acquire.do(text)

        params = self.getParams(text, self.tk)
        URL = baseURL + params

        #用response的时候解码中译英的json出现了乱码
        #response = self.session.get(url, proxies=self.proxy\
                # , timeout=self.timeout)
        #content = response.content.decode('utf8')

        if self.proxy != None:

            cprint('<proxy>', 'blue')
            handler = urllib.request.ProxyHandler( self.proxy )
            opener = urllib.request.build_opener( handler )
            urllib.request.install_opener(opener)

        req = urllib.request.Request(URL, headers=self.getHeaders())

        try:
            response = urllib.request.urlopen(req, timeout=self.timeout)
        except Exception as e:
            raise Exception(e);

        content = gzip.GzipFile(fileobj=response).read().decode('utf8')

        print()
        return json.loads(content)

    def getMoreTran(self, data, exclude):

        try:
            string1 = ''
            string2 = ''

            #词性对应的中文意思
            string1 = data[0][0]+':'+','.join(data[0][1])
            data = data[0][2:]

            #查找单词的中文翻译对应的其他单词
            for word in data[0]:
                try:
                    word[1].remove(exclude)
                    string2 = word[0]+':'+','.join((word[1]))+' | '+string2
                except Exception:
                    pass

            return string1+' | '+string2

        except TypeError:
            pass

    def getSynonym(self, data, flag=1):

        try:
            string = ''
            wlist = []
            for i,element in enumerate(data[0][1][0][0]):
                if flag and i > 8:
                    break;

                if flag:
                    string += element + ','
                else:
                    string += element

            return string

        except TypeError:
            pass

    def extractData(self, dataList, host):

        #有用数据下标 0, 1, 11, 12
        #0: 返回到界面的直接翻译
        #1: 各词性的其他翻译
        #11:不同词性的同义词
        #12:英语解释

        #返回的翻译结果
        cprint('>> ' + dataList[0][0][1] + \
                ': ' + dataList[0][0][0], 'cyan')

        string = ''
        #单词的英语解释
        if len(dataList) > 12:
            cprint('    ', end='')
            string = self.getSynonym(dataList[12], 0)

            if string:  
                cprint('英语解释:'+string,'green')

        #词性及中文翻译
        string = self.getMoreTran(dataList[1], dataList[0][0][1])
        cprint(string, 'red')

        if len(dataList) > 12:
            if dataList[11] is not None:
                print()
                cprint('    同义词: ', 'blue',  end='')
                string = self.getSynonym(dataList[11])
                if string:
                    cprint('    '+string,'green')

    def pic2char(self, dirname):

        host = "https://translate.google.cn/"
        proxy = {'http':'localhost:8123'}

        while True:
            name = self.ScanNewFile(dirname)
            self.WaitForFileSavedSuccessfully()
            data = self.ExtractText(name);
            os.system("rm -rf "+name)
            return data
