from translate.package.Translator import Translator

tran = Translator(targetLang='zh-CN')
data = tran.getTran('test')
print(data)
