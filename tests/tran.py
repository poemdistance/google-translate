import sys
sys.path.append('../translate')

from Translator import Translator


host = "https://translate.google.com/"
proxy = { 'https':'localhost:8123' }

tran = Translator(targetLang='zh-CN', host=host, proxy=proxy)

#获取原始json数据
RowData = tran.getTran('Test')
print(RowData)


tran = Translator(targetLang='en', host=host, proxy=proxy)

#获取原始json数据
RowData = tran.getTran('测试')
print(RowData)

