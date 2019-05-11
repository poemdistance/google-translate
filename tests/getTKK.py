import re
import os
import math
import time
import pickle
import requests
import urllib
from bs4 import BeautifulSoup
import urllib.parse
from urllib.request import urlopen, Request

class getTKK(object):
    def __init__(self, proxy=None, tkk='0'):
        self.tkk = tkk
        self.proxy = proxy

    def get(self):

        if self.tkk == '0' and os.path.exists('./.tkk'):
            with open('./.tkk', 'rb') as f:
                self.tkk = pickle.load(f)
                print('found .tkk file, load firstly, tkk=', self.tkk)

        now = math.floor(int(time.time()) / 3600)
        if self.tkk and int(self.tkk.split('.')[0]) == now:
            if os.path.exists('./.tkk'):
                print('Tkk file still useful, will not change')
            return

        BaseURL = "https://translate.google.cn/#view=\
                   home&op=translate&sl=en&tl=zh-CN&text="

        text = 'test'

        text = urllib.parse.quote(text)
        URL = BaseURL+text
        header = { 'User-Agent': 'Mozilla/5.0' }

        #add header to prevent being discerned as bot
        html = requests.get(URL, headers=header, proxies=self.proxy).content
        html = html.decode('utf8')

        soup = BeautifulSoup( html, 'html.parser' )
        string = soup.script.get_text()

        #Find the string: tkk:'xxxx.xxxx', and then extract the number
        ret = re.search(r'\d+\.\d+', 
                re.search(r'tkk:\'\d+\.\d+\'', html).group()).group()

        print('Got TKK=', ret)
        return ret

getTKK().get()
