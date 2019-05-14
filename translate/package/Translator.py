#-*-Coding:utf-8-*-
import os
import sys
import time
import gzip
import json
import urllib
import requests
from termcolor import colored, cprint
from time import time
from translate.package.getTK import TokenAcquirer
from PIL import Image, PILLOW_VERSION

class Translator(object):

    def __init__(self, targetLang='zh-CN', \
            proxy=None, timeout=3, host='https://translate.google.cn'):
        self.host = host
        self.targetLang = targetLang
        self.proxy = proxy
        self.session = requests.Session()
        self.timeout = timeout

    def getcookie(self):
        cookie = {
                'cookie':'182=AX2oNMyUeRd8RJXqRNGS617RPfUuMCNowbg\
                 BE2A688Le5wzwjkV1sudMHSW0xyEqe9TKPfeit7fAoF6vwth\
                 qpX7NToId4xhiP_J0QQi3wasA44rD8rGLMA3_DQcvrtmJyXh\
                 0enZS9bFP8BBxC1vtQDah39bL1ZbuNLhJ9CH2yQQ'
                }

        return cookie

    def getParams(self, word, token ):

        key = []
        val = []

        cprint('Target lanuage = %s' % self.targetLang, 'blue')
        print()

        if self.targetLang == 'en':
            key = ['client','sl','tl','hl','dt','dt','dt','dt','dt','dt','dt',\
                   'dt','dt','dt','dt','otf','pc','ssel','tsel','kc','tk','q']

            val=['webapp','zh-CN','en','en','at','bd','ex','ld','md', 'qca',
                    'rw','rm','ss','t','gt','1','1','3','5','2',token,word]

        elif self.targetLang == 'zh-CN':
            key = ['client','sl','tl','hl','dt','dt','dt','dt','dt','dt','dt',\
                   'dt','dt','dt','swap','otf','pc','ssel','tsel','kc','tk','q']

            val=['webapp','en','zh-CN','en','at','bd','ex','ld','md',\
                 'qca','rw','rm','ss','t','1','1','1','5','5','2',token,word]
        else:
            print('Not support target language: %s yet' % self.targetLang)

        result = ''

        for i in range(len(key)-1):
            result += key[i] + '=' + val[i] + '&'

        result += key[len(key)-1]+ '=' + urllib.parse.quote_plus(word)
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
            'referer': 'https://translate.google.com/',
            'Connection': 'keep-alive',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 \
                           (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36',
                }

        return headers

    def ScanNewFile():
        inTime = time.time()
        try:
            while True:
                with os.scandir('./') as entries:
                    for entry in entries :
                        if entry.is_file():
                            attrs = entry.stat()
                            if attrs.st_mtime > inTime:
                                print('Found new file: %s' % entry.name)
                                return os.path.abspath('./'+entry.name)
        except FileNotFoundError as err:
            print(str(err))
            ScanNewFile()

    def ExtractText(fileName):
        print('Prepare to open image: %s' % fileName)
        image = Image.open(fileName)
        text = pytesseract.image_to_string(image)
        print(text)
        return text

    def GetTranslation(text):
        URL = baseURL + text
        proxySupport = urllib.request.ProxyHandler({'socks5':'https://127.0.0.1:1080'})
        opener = urllib.request.build_opener(proxySupport)
        urllib.request.install_opener(opener)
        #html = urlopen(URL)

        #bsobj = BeautifulSoup(html, 'lxml')
        #print(bsobj.decode('utf8'))

    def PrintTran(tran):
        print(tran)

    def WaitForFileSavedSuccessfully():
        time.sleep(0.1)

    def getTran(self, text):

        baseURL = 'https://translate.google.cn/'

        self.acquire = TokenAcquirer(session=self.session, proxy=self.proxy, 
                timeout=self.timeout, host=self.host)
        self.tk = self.acquire.do(text)

        header = self.getHeaders()
        params = self.getParams(text, self.tk)

        URL = baseURL + params

        #用response的时候解码中译英的json出现了乱码
        #if self.targetLang == 'zh-CN':
        #    response = self.session.get(url, proxies=self.proxy, timeout=self.timeout)
        #    content = response.content.decode('utf8')

        #elif self.targetlang == 'en':

        if self.proxy != None:

            print()
            cprint('Setting proxy...', 'blue')
            handler = urllib.request.ProxyHandler( self.proxy )
            opener = urllib.request.build_opener( handler )
            urllib.request.install_opener(opener)
            cprint('Setting proxy successful...', 'blue')
            print()

        cprint('Preparing to get data from server...', 'blue')

        req = urllib.request.Request(URL, headers=header)
        response = urllib.request.urlopen(req)
        content = gzip.GzipFile(fileobj=response).read().decode('utf8')

        cprint('Got data successful...', 'blue')
        print()
        return json.loads(content)

"""
#-*-Test code with no proxy
host = 'https://translate.google.cn' #default host
translator = Translator(targetLang='en', timeout=3, proxy=None)
data = translator.getTran("her's")
print(data)
print()

"""
"""
translator = Translator(targetLang='zh-CN', timeout=3, proxy=None)
data = translator.getTran("Just go forward, don't look back" )
print(data)
"""
"""
#-*-Test code with  proxy
host = 'https://translate.google.com'
proxy = { 'https':'localhost:8123' }

translator = Translator(targetLang='en', timeout=3, proxy=proxy, host=host)
data = translator.getTran('老巷的墙')
print(data)
print()

translator = Translator(targetLang='zh-CN', timeout=3, proxy=proxy, host=host)
data = translator.getTran("Just go forward, don't look back" )
print(data)
"""
