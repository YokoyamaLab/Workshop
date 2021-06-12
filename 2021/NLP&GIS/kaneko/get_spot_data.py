import requests
from  bs4 import BeautifulSoup
import time
import sys

def get_spot_data(url):
    try:
        res = requests.get(url)
    except:
        return None,None,None,None,None
    else:
        soup = BeautifulSoup(res.text, 'html.parser')
        # タイトル、リード文、概要、緯度、経度の取得
        title_text = soup.find('title')
        lead_sentence = soup.find('p')
        overview = soup.select('h2:contains("概要") ~ p')
        overview_list = [t.get_text(strip=True) for t in overview]
        overview_str = ''.join(overview_list)
        latitude = soup.find('span', {'class': 'latitude'})
        longitude = soup.find('span', {'class': 'longitude'})
        
        # データを取得できなかったら長さ0の文字列に置き換える
        if title_text is None:
            title_text = ''
        else:
            title_text = title_text.get_text()
        if lead_sentence is None:
            lead_sentence = ''
        else:
            lead_sentence = lead_sentence.text
        if latitude is None:
            latitude = ''
        else:
            latitude = latitude.get_text()
        if longitude is None:
            longitude = ''
        else:
            longitude = longitude.get_text()
        
        return title_text,lead_sentence,overview_str,latitude,longitude

def main():
    if len(sys.argv) == 1:
        url = 'https://ja.wikipedia.org/wiki/%E6%81%B5%E6%AF%94%E5%AF%BF%E3%82%AC%E3%83%BC%E3%83%87%E3%83%B3%E3%83%97%E3%83%AC%E3%82%A4%E3%82%B9'
    else:
        url = sys.argv[1]
    
    title,lead_sentence,overview,latitude,longitude = get_spot_data(url)
    print(title)
    print(lead_sentence)
    print(overview)
    print(latitude)
    print(longitude)

if __name__ == '__main__':
    main()
