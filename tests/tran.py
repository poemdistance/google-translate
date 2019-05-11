import sys
sys.path.append('../translate')

from Translator import Translator

tran = Translator(targetLang='zh-CN')
RowData = tran.getTran('Test')
print(RowData)


tran = Translator(targetLang='en')
RowData = tran.getTran('测试')
print(RowData)

