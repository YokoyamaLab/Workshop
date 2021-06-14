# use 'practice_nlpgeo' environment anaconda

from os import read, write
import requests
from bs4 import BeautifulSoup
import time
import json
import codecs
import csv
import geocoder

with open('exception_list.csv') as f:
    reader = csv.reader(f)
    exception_list = [row for row in reader]
    exception = exception_list[0]

def comp_lead(text):
    if text in exception:
        return False
    elif "座標:" in text:
        return False
    else:
        return True

def get_latlon(title):
    l = geocoder.osm(title, timeout=5.0)
    if l.latlng==None:
        l=None
    else:
        l = str(l.latlng[0])+' '+str(l.latlng[1])
    return l

def main():
    main_url = 'https://ja.wikipedia.org/wiki/Category:%E6%9D%B1%E4%BA%AC%E9%83%BD%E3%81%AE%E8%A6%B3%E5%85%89%E5%9C%B0'
    main_res = requests.get(main_url)
    main_html = BeautifulSoup(main_res.text, 'html.parser')

    # json
    jsonfile = codecs.open('tourist_spot.json','w','utf-8')
    data={}

    # spot url
    for n in main_html.select('div#mw-pages a'):
        target_url = 'https://ja.wikipedia.org' + n.get('href')
        target_res=requests.get(target_url)
        target_html=BeautifulSoup(target_res.text,'html.parser')
        time.sleep(1)

        #title
        title=target_html.select_one('h1')
        if title != None:
            title = title.get_text()
        print(title)

        for a in target_html.select('div.mw-parser-output'):
            # lead
            lead = None
            during_lead = False
            for l in a.contents:
                if l.name == 'p' and comp_lead(l.get_text()) and (not during_lead):
                    during_lead = True
                    lead=l.get_text()
                elif during_lead and l.name == 'p':
                    lead=lead+l.get_text()
                elif during_lead and l.name != 'p':
                    during_lead = False
                    break
            print(lead)
            time.sleep(1)

            # overview
            overview = None
            during_overview=False
            for o in a.contents:
                if o.name == 'h2' and o.get_text() == '概要[編集]':
                    during_overview = True
                elif during_overview and o.name == 'p':
                    if overview == None:
                        overview = o.get_text()
                    else:
                        overview = overview + o.get_text()
                elif o.name == 'h2' and o.get_text() != '概要[編集]':
                    during_overview = False
            print(overview)
            time.sleep(1)

        # latitude longitude
        latitude = target_html.select_one('span.latitude')
        longitude = target_html.select_one('span.longitude')
        latlon = target_html.select_one('[title="この位置の地図や航空写真などをリンクするページを表示します"]')

        if latitude != None and longitude != None and len(latitude)>3 and len(longitude)>3:
            latitude = latitude.get_text()
            longitude = longitude.get_text()
            latlon = str(latitude) + ' ' + str(longitude)
        elif latlon != None and len(latlon)>6:
            latlon = latlon.get_text()
        else:
            latlon = get_latlon(title)
        print(latlon)
        time.sleep(1)

        # spot address
        # 以下2つを満たす場合に手動
        # 条件A.そのページに住所の記載がある
        # 条件B.そのページに緯度経度情報の記載がない
        address = None

        # json
        # data = {'title':title, 'lead':lead, 'overview':overview, 'latlon':latlon, 'address':address}
        # json.dump(data,jsonfile,ensure_ascii=False,indent=len(data))

        data[title] = {'title': title,'lead':lead, 'overview':overview, 'latlon':latlon, 'address':address}
        time.sleep(1)

    json.dump(data, jsonfile, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()

