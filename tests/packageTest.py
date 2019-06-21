from translate.package.Translator import Translator

host = "https://translate.google.com/"
proxy = { 'https':'localhost:8123' }

tran = Translator(targetLang='zh-CN', host=host, proxy=proxy)
data = tran.getTran('test')
print(data)
