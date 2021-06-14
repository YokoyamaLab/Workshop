import csv
from os import write

with open('exception_list.csv','w') as file:
    writer = csv.writer(file)
    writer.writerow([
        'この記事には複数の問題があります。改善やノートページでの議論にご協力ください。\n',
        'この記事は検証可能な参考文献や出典が全く示されていないか、不十分です。出典を追加して記事の信頼性向上にご協力ください。\n',
        '\n'
        ])

with open('exception_list.csv') as file:
    print(file.read())
