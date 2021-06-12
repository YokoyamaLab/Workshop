import requests
import time
from bs4 import BeautifulSoup
import csv
import get_spot_data

res = requests.get('https://ja.wikipedia.org/wiki/Category:%E6%9D%B1%E4%BA%AC%E9%83%BD%E3%81%AE%E8%A6%B3%E5%85%89%E5%9C%B0')
# レスポンスの HTML から BeautifulSoup オブジェクトを作る
soup = BeautifulSoup(res.text, 'html.parser')

# ページに含まれるリンクを全て取得する
urls = [url.get('href') for url in soup.find_all('a')]
# print(urls)

csv_file = open('tokyo_spot_data.csv','w')
writer = csv.writer(csv_file, lineterminator='\n')

for url in urls:
    if url is None:
        continue
    if 'Category:' in url:
        continue
    if 'https://ja.wikipedia.org' not in url:
        url = 'https://ja.wikipedia.org' + url
    
    title_text, lead_sentence,overview,latitude,longitude = get_spot_data.get_spot_data(url)

    # データを取得したらcsvファイルに保存
    if title_text is not None and lead_sentence is not None and overview is not None and latitude is not None and longitude is not None:
        writer.writerow([title_text, lead_sentence,overview,latitude,longitude])
        print(url)
    time.sleep(5)

csv_file.close()
